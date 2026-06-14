#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPERIMENTO FINAL — análise objetiva automática (um único script).

Baseado em avaliador/avaliador.py do projeto (mesmas bibliotecas e métricas),
adaptado para a estrutura do experimento final:

    docs/Inferencias finais/Audios/<modelo>/outputs_final_experiment/<condicao>/<vN>/NNN.wav
      <modelo>   = fishspeech | unsloth | xtts
      <condicao> = original (checkpoint ANTES do fine-tune) | ajustado (COM fine-tune)
      <vN>       = v1 | v2 | v3  (3 repetições, seeds 42/123/456)
      NNN        = 001..100  (linha N de sentenças.txt = ground truth)

Faz tudo de uma vez:
  1) varre os 1800 áudios (3 x 2 x 3 x 100)
  2) Whisper STT (small, pt) + distância/similaridade de Levenshtein vs ground truth
  3) preditores de MOS: NISQA + DNSMOS (torchmetrics)  [MOSA-Net opcional, ver hook]
  4) CSV1: todas as métricas, 1800 linhas
  5) CSV2: melhor das 3 repetições por (modelo,condicao,sentença) — score composto Lev+MOS
  6) gráficos (PNG) + conclusoes_preliminares.md (Δ ajustado-original + Wilcoxon)

Requisitos (os mesmos do seu avaliador.py):
  pip install torch torchaudio openai-whisper torchmetrics pandas numpy matplotlib scipy tqdm

Uso:
  python experimento_final.py                  # pipeline completo (resumível)
  python experimento_final.py --limit 30       # teste rápido (30 áudios)
  python experimento_final.py --overwrite      # recalcula tudo
  python experimento_final.py --only-agg       # só refaz CSV2/gráficos a partir do CSV1
  python experimento_final.py --device cuda
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import traceback
from pathlib import Path

# ===========================================================================
# CONFIGURAÇÃO
# ===========================================================================
EXP_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXP_DIR.parent
AUDIO_BASE = REPO_ROOT / "docs" / "Inferencias finais" / "Audios"
SENTENCES_FILE = AUDIO_BASE / "sentenças.txt"

RESULTS_DIR = EXP_DIR / "resultados"
PLOTS_DIR = RESULTS_DIR / "plots"
CSV1 = RESULTS_DIR / "csv1_todas_metricas.csv"
CSV2 = RESULTS_DIR / "csv2_melhor_de_3.csv"
CONCLUSOES_MD = RESULTS_DIR / "conclusoes_preliminares.md"
LOG_PATH = RESULTS_DIR / "experimento_final.log"

MODELOS = ["fishspeech", "unsloth", "xtts"]
CONDICOES = ["original", "ajustado"]
VARIACOES = ["v1", "v2", "v3"]
N_SENTENCAS = 100
SUBPASTA = "outputs_final_experiment"

WHISPER_MODEL = "small"
WHISPER_LANGUAGE = "pt"

# MOS principal usado na seleção composta e nos gráficos (ordem de preferência).
MOS_PREFERENCIA = ["mosanet_mos", "nisqa_overall", "dns_ovrl"]
# Pesos do score composto do CSV2 (melhor das 3). Ajuste se quiser priorizar
# inteligibilidade (Levenshtein) sobre qualidade (MOS) ou vice-versa.
PESO_LEV = 0.5
PESO_MOS = 0.5

# Opcional: MOSA-Net (Zezario et al., 2024). Se não configurar, fica em branco
# e a seleção/gráficos usam NISQA como MOS principal. Ver mosanet/README.md.
USAR_MOSANET = False

CAMPOS = [
    "modelo", "condicao", "variacao", "indice", "arquivo",
    "texto_original", "texto_transcrito", "duracao_s",
    "lev_dist", "lev_sim",
    "mosanet_mos",
    "nisqa_overall", "nisqa_noisiness", "nisqa_discontinuity",
    "nisqa_coloration", "nisqa_loudness",
    "dns_sig", "dns_bak", "dns_ovrl",
    "mos_principal", "mos_principal_fonte",
    "status", "erro",
]


# ===========================================================================
# UTILIDADES (portadas do avaliador.py)
# ===========================================================================
def log(msg: str):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(str(msg).rstrip() + "\n")
    print(msg, flush=True)


def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            ins = current[j - 1] + 1
            dele = previous[j] + 1
            sub = previous[j - 1] + (0 if ca == cb else 1)
            current.append(min(ins, dele, sub))
        previous = current
    return previous[-1]


def lev_similarity(ref_raw: str, hyp_raw: str):
    """(dist, sim) sobre texto normalizado. sim = 1 - dist/max(len_ref,len_hyp).
    Reproduz a Tabela 2.4 da dissertação ('Frei Damião' x 'Freio de Caminhão'
    -> dist 6, max 17 -> 0.65)."""
    ref, hyp = normalize_text(ref_raw), normalize_text(hyp_raw)
    dist = levenshtein(ref, hyp)
    sim = 1.0 - dist / max(len(ref), len(hyp), 1)
    return dist, max(0.0, sim)


def load_audio_mono16k(path, target_sr=16000):
    """Carrega WAV como tensor torch mono [1, n] no target_sr.
    Usa librosa/soundfile (não depende do torchcodec, que mudou no torchaudio
    novo). librosa.load já faz mono + resample."""
    import torch
    import numpy as np
    import librosa
    y, sr = librosa.load(str(path), sr=target_sr, mono=True)  # float32 já no target_sr
    wav = torch.from_numpy(np.ascontiguousarray(y, dtype=np.float32)).unsqueeze(0)
    return wav, target_sr, wav.shape[-1] / float(target_sr)


def compute_nisqa(wav, sr):
    """NISQA tem um teto de janelas de mel-espectrograma (áudios muito longos
    estouram). Se acontecer, trunca progressivamente e tenta de novo."""
    from torchmetrics.functional.audio.nisqa import non_intrusive_speech_quality_assessment as tm_nisqa
    x = wav.squeeze(0)
    for max_s in (None, 20, 12, 8):
        seg = x if max_s is None else x[..., : int(max_s * sr)]
        try:
            scores = tm_nisqa(seg, fs=sr)
            return tuple(float(v) for v in scores.tolist())  # overall, noisiness, discont, coloration, loudness
        except RuntimeError as e:
            if "mel spectrogram windows" in str(e) or "shorter audio" in str(e):
                continue  # áudio comprido demais: tenta com janela menor
            raise
    raise RuntimeError("NISQA: áudio longo demais mesmo após truncar para 8s")


def make_dnsmos(sr):
    from torchmetrics.audio.dnsmos import DeepNoiseSuppressionMeanOpinionScore
    return DeepNoiseSuppressionMeanOpinionScore(fs=sr, personalized=False)


def compute_dnsmos(metric, wav):
    import torch
    out = metric(wav.squeeze(0))
    vals = out.flatten().tolist() if torch.is_tensor(out) else list(out)
    sig = bak = ovr = None
    if len(vals) >= 3:
        sig, bak, ovr = float(vals[0]), float(vals[1]), float(vals[2])
    return sig, bak, ovr


def make_mosanet(device):
    """Hook opcional do MOSA-Net. Retorna objeto com .predict(wav, sr)->float
    ou None. Ver Experimento final/mosanet/README.md."""
    if not USAR_MOSANET:
        return None
    try:
        sys.path.insert(0, str((EXP_DIR / "mosanet").resolve()))
        import mosanet_wrapper
        return mosanet_wrapper.MosaNet(repo_dir=EXP_DIR / "mosanet" / "MOSA-Net-Cross-Domain", device=device)
    except Exception as e:
        log(f"[MOSA-Net indisponível, seguindo sem ele] {e}")
        return None


# ===========================================================================
# VARREDURA
# ===========================================================================
def load_sentences():
    if not SENTENCES_FILE.exists():
        raise FileNotFoundError(f"sentenças.txt não encontrado: {SENTENCES_FILE}")
    linhas = SENTENCES_FILE.read_text(encoding="utf-8").splitlines()
    while linhas and not linhas[-1].strip():
        linhas.pop()
    return linhas


def iter_audios(sentences):
    for modelo in MODELOS:
        for cond in CONDICOES:
            for v in VARIACOES:
                base = AUDIO_BASE / modelo / SUBPASTA / cond / v
                for idx in range(1, N_SENTENCAS + 1):
                    p = base / f"{idx:03d}.wav"
                    texto = sentences[idx - 1] if idx - 1 < len(sentences) else ""
                    yield modelo, cond, v, idx, p, texto


def key(modelo, cond, v, idx):
    return f"{modelo}|{cond}|{v}|{idx:03d}"


def pick_mos(row):
    for c in MOS_PREFERENCIA:
        val = row.get(c)
        if val not in (None, "") and not (isinstance(val, float) and val != val):
            return val, c
    return "", ""


# ===========================================================================
# FASE 1 — MÉTRICAS (STT + Levenshtein + NISQA + DNSMOS) -> CSV1
# ===========================================================================
def processar_item(modelo, cond, v, idx, path_str, texto, wmodel, dnsmos, mosanet, fp16):
    """Calcula todas as métricas de UM áudio e devolve a linha (dict). Reusado
    no modo sequencial e nos workers paralelos."""
    path = Path(path_str)
    row = {c: "" for c in CAMPOS}
    row.update({"modelo": modelo, "condicao": cond, "variacao": v, "indice": idx,
                "arquivo": str(path.relative_to(AUDIO_BASE)), "texto_original": texto})
    if not path.exists():
        row["status"] = "missing"; row["erro"] = "arquivo não encontrado"; return row
    try:
        wav, sr, dur = load_audio_mono16k(path)
        row["duracao_s"] = round(dur, 3)
        hyp = (wmodel.transcribe(str(path), language=WHISPER_LANGUAGE, fp16=fp16).get("text") or "").strip()
        dist, sim = lev_similarity(texto, hyp)
        row["texto_transcrito"] = hyp; row["lev_dist"] = dist; row["lev_sim"] = round(sim, 4)
        try:
            no, nn, nd, nc, nl = compute_nisqa(wav, sr)
            row.update({"nisqa_overall": round(no, 4), "nisqa_noisiness": round(nn, 4),
                        "nisqa_discontinuity": round(nd, 4), "nisqa_coloration": round(nc, 4),
                        "nisqa_loudness": round(nl, 4)})
        except Exception as e:
            print(f"[NISQA erro] {path.name}: {e}", flush=True)
        if dnsmos is not None:
            try:
                sg, bk, ov = compute_dnsmos(dnsmos, wav)
                if sg is not None:
                    row.update({"dns_sig": round(sg, 4), "dns_bak": round(bk, 4), "dns_ovrl": round(ov, 4)})
            except Exception as e:
                print(f"[DNSMOS erro] {path.name}: {e}", flush=True)
        if mosanet is not None:
            try:
                row["mosanet_mos"] = round(float(mosanet.predict(wav, sr)), 4)
            except Exception as e:
                print(f"[MOSA-Net erro] {path.name}: {e}", flush=True)
        mosv, fonte = pick_mos(row)
        row["mos_principal"] = mosv if mosv == "" else round(float(mosv), 4)
        row["mos_principal_fonte"] = fonte
        row["status"] = "ok"
    except Exception as e:
        row["status"] = "error"; row["erro"] = str(e)
    return row


def _carregar_modelos(device):
    import whisper
    wmodel = whisper.load_model(WHISPER_MODEL, device=device)
    try:
        dnsmos = make_dnsmos(16000)
    except Exception as e:
        dnsmos = None; print(f"[DNSMOS indisponível, seguindo com NISQA] {e}", flush=True)
    mosanet = make_mosanet(device)
    return wmodel, dnsmos, mosanet


def _worker_shard(payload):
    """Executado em cada processo: carrega modelos uma vez e processa seu lote,
    gravando num CSV-parte próprio (resumível). Retorna (wid, ok, total)."""
    import os
    wid = payload["wid"]; items = payload["items"]; device = payload["device"]
    fp16 = payload["fp16"]; part_path = payload["part"]; nthreads = payload["nthreads"]
    try:
        import torch; torch.set_num_threads(max(1, nthreads))
    except Exception:
        pass
    feitos = set()
    if os.path.exists(part_path):
        with open(part_path, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r.get("status") == "ok":
                    feitos.add(key(r["modelo"], r["condicao"], r["variacao"], int(r["indice"])))
    wmodel, dnsmos, mosanet = _carregar_modelos(device)
    novo = not os.path.exists(part_path)
    f = open(part_path, "a", newline="", encoding="utf-8-sig")
    w = csv.DictWriter(f, fieldnames=CAMPOS)
    if novo:
        w.writeheader()
    ok = 0
    for j, (modelo, cond, v, idx, path_str, texto) in enumerate(items, 1):
        if key(modelo, cond, v, idx) in feitos:
            continue
        row = processar_item(modelo, cond, v, idx, path_str, texto, wmodel, dnsmos, mosanet, fp16)
        w.writerow(row); f.flush()
        if row["status"] == "ok":
            ok += 1
        print(f"[worker {wid}] {j}/{len(items)} {row.get('status')} "
              f"lev_sim={row.get('lev_sim','')} mos={row.get('mos_principal','')} | {row.get('arquivo')}", flush=True)
    f.close()
    return wid, ok, len(items)


def _merge_parts(parts_dir, manter_existente):
    import glob
    import pandas as pd
    frames = []
    if manter_existente and CSV1.exists():
        frames.append(pd.read_csv(CSV1, encoding="utf-8-sig", dtype=str))
    for pf in sorted(glob.glob(str(parts_dir / "csv1_part_*.csv"))):
        try:
            frames.append(pd.read_csv(pf, encoding="utf-8-sig", dtype=str))
        except Exception:
            pass
    if not frames:
        return
    df = pd.concat(frames, ignore_index=True)
    df["_k"] = (df["modelo"] + "|" + df["condicao"] + "|" + df["variacao"] + "|" + df["indice"].astype(str))
    df["_ok"] = (df["status"] == "ok").astype(int)
    df = (df.sort_values("_ok").drop_duplicates("_k", keep="last").drop(columns=["_k", "_ok"]))
    om = {m: i for i, m in enumerate(MODELOS)}; oc = {c: i for i, c in enumerate(CONDICOES)}
    df["_m"] = df["modelo"].map(om); df["_c"] = df["condicao"].map(oc)
    df["indice"] = df["indice"].astype(int)
    df = df.sort_values(["_m", "_c", "indice", "variacao"]).drop(columns=["_m", "_c"])
    df.to_csv(CSV1, index=False, encoding="utf-8-sig")


def fase_metricas(args):
    import torch
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    fp16 = device == "cuda"
    import os as _os
    pedido = max(1, int(getattr(args, "workers", 5) or 5))
    ncpu = _os.cpu_count() or 1
    workers = pedido
    # GPU: paralelizar processos numa única GPU costuma só competir por VRAM
    if device == "cuda" and workers > 1:
        log(f"[aviso] Em GPU, {workers} processos competem pela mesma VRAM. "
            f"Geralmente 1 worker em GPU já é mais rápido que vários na CPU. Mantendo {workers} (reduza se faltar VRAM).")
    # CPU: não adianta mais processos que núcleos
    if device == "cpu" and workers > ncpu:
        log(f"[aviso] Você pediu {workers} áudios simultâneos, mas a máquina tem só {ncpu} núcleos. "
            f"Reduzindo para {ncpu} (mais que isso só geraria disputa de CPU). "
            f"Para forçar, passe --workers {workers} de novo após ajustar o hardware.")
        workers = ncpu
    if device == "cpu" and workers >= 4:
        log(f"[aviso] {workers} processos carregam o Whisper cada um (~1–2 GB de RAM por processo, "
            f"~{workers*2} GB no total). Se travar/ficar sem memória, rode com --workers 2 ou 3.")
    log(f"Dispositivo: {device} | Whisper: {WHISPER_MODEL} | fp16={fp16} | workers={workers} (pedido: {pedido}, núcleos: {ncpu})")

    sentences = load_sentences()
    log(f"Sentenças: {len(sentences)} (esperado {N_SENTENCAS})")

    feitos = set()
    if CSV1.exists() and not args.overwrite:
        with CSV1.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r.get("status") == "ok":
                    feitos.add(key(r["modelo"], r["condicao"], r["variacao"], int(r["indice"])))
        log(f"Retomando: {len(feitos)} áudios já processados serão pulados.")

    itens = list(iter_audios(sentences))
    if args.limit:
        itens = itens[: args.limit]
    pend = [(m, c, v, i, str(p), t) for (m, c, v, i, p, t) in itens
            if key(m, c, v, i) not in feitos]
    log(f"A processar: {len(pend)} (de {len(itens)})")
    if not pend:
        log("Nada a processar (tudo já feito). Use --overwrite para refazer.")
        return

    # -------- modo sequencial --------
    if workers <= 1:
        modo = "w" if (args.overwrite or not CSV1.exists()) else "a"
        fout = CSV1.open(modo, newline="", encoding="utf-8-sig")
        writer = csv.DictWriter(fout, fieldnames=CAMPOS)
        if modo == "w":
            writer.writeheader()
        log("Carregando modelos (Whisper + MOS)...")
        wmodel, dnsmos, mosanet = _carregar_modelos(device)
        ok = err = 0
        for n, it in enumerate(pend, 1):
            row = processar_item(it[0], it[1], it[2], it[3], it[4], it[5], wmodel, dnsmos, mosanet, fp16)
            writer.writerow(row); fout.flush()
            if row["status"] == "ok":
                ok += 1
            else:
                err += 1
            log(f"[{n}/{len(pend)}] {row.get('status')} | lev_sim={row.get('lev_sim','')} "
                f"mos={row.get('mos_principal','')} ({row.get('mos_principal_fonte','')}) | {row.get('arquivo')}")
        fout.close()
        log(f"FASE MÉTRICAS fim. ok={ok} erros={err} -> {CSV1}")
        return

    # -------- modo paralelo (workers > 1) --------
    import concurrent.futures
    import multiprocessing
    import os
    parts_dir = RESULTS_DIR / "_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    shards = [[] for _ in range(workers)]
    for k_, it in enumerate(pend):
        shards[k_ % workers].append(it)
    total_threads = os.cpu_count() or workers
    nthreads = max(1, total_threads // workers)
    payloads = [{"wid": w, "items": shards[w], "device": device, "fp16": fp16,
                 "part": str(parts_dir / f"csv1_part_{w}.csv"), "nthreads": nthreads}
                for w in range(workers) if shards[w]]
    log(f"Paralelo: {len(payloads)} processos, ~{nthreads} threads cada. "
        f"(Atenção: cada processo carrega os modelos; cuidado com a RAM.)")
    ctx = multiprocessing.get_context("spawn")
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(payloads), mp_context=ctx) as ex:
        for wid, ok, tot in ex.map(_worker_shard, payloads):
            log(f"[worker {wid}] concluído: {ok}/{tot} ok")
    _merge_parts(parts_dir, manter_existente=(not args.overwrite))
    log(f"FASE MÉTRICAS (paralela) fim -> {CSV1}")


# ===========================================================================
# FASE 2 — CSV2 (melhor das 3) + gráficos + conclusões
# ===========================================================================
def _save_csv(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")
    pt = Path(path).with_name(Path(path).stem + "_ptbr-excel.csv")
    df.to_csv(pt, index=False, sep=";", decimal=",", encoding="utf-8-sig")


def fase_agregacao():
    import numpy as np
    import pandas as pd

    if not CSV1.exists():
        log(f"[ERRO] {CSV1} não existe. Rode a fase de métricas primeiro."); return
    df = pd.read_csv(CSV1, encoding="utf-8-sig")
    for c in ["lev_sim", "mos_principal", "nisqa_overall", "dns_ovrl", "lev_dist"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- CSV2: melhor das 3 por (modelo,condicao,indice) ----
    def minmax(s):
        v = s.astype(float); a, b = v.min(), v.max()
        if pd.isna(a) or pd.isna(b) or a == b:
            return pd.Series(np.where(v.notna(), 1.0, np.nan), index=v.index)
        return (v - a) / (b - a)

    escolhidos = []
    for (m, c, i), g in df.groupby(["modelo", "condicao", "indice"], sort=False):
        g = g.copy()
        tem_lev = g["lev_sim"].notna().any()
        tem_mos = g["mos_principal"].notna().any() if "mos_principal" in g else False
        lev01 = minmax(g["lev_sim"]) if tem_lev else pd.Series(np.nan, index=g.index)
        mos01 = minmax(g["mos_principal"]) if tem_mos else pd.Series(np.nan, index=g.index)
        if tem_lev and tem_mos:
            score = PESO_LEV * lev01.fillna(0) + PESO_MOS * mos01.fillna(0)
        elif tem_lev:
            score = lev01
        elif tem_mos:
            score = mos01
        else:
            score = pd.Series(0.0, index=g.index)
        g["score_composto"] = score.round(4)
        g["lev_norm01"] = lev01.round(4); g["mos_norm01"] = mos01.round(4)
        ordem_v = {v: k for k, v in enumerate(VARIACOES)}
        g["_v"] = g["variacao"].map(ordem_v)
        g = g.sort_values(["score_composto", "lev_sim", "mos_principal", "_v"],
                          ascending=[False, False, False, True])
        escolhidos.append(g.iloc[0].drop(labels=["_v"]))
    c2 = pd.DataFrame(escolhidos).rename(columns={"variacao": "variacao_escolhida"})
    frente = ["modelo", "condicao", "indice", "variacao_escolhida", "score_composto",
              "lev_sim", "mos_principal", "mos_principal_fonte"]
    frente = [x for x in frente if x in c2.columns]
    c2 = c2[frente + [x for x in c2.columns if x not in frente]]
    om = {m: k for k, m in enumerate(MODELOS)}; oc = {c: k for k, c in enumerate(CONDICOES)}
    c2["_m"] = c2["modelo"].map(om); c2["_c"] = c2["condicao"].map(oc)
    c2 = c2.sort_values(["_m", "_c", "indice"]).drop(columns=["_m", "_c"])
    _save_csv(c2, CSV2)
    log(f"CSV2 salvo: {CSV2} ({len(c2)} linhas) | variações: {c2['variacao_escolhida'].value_counts().to_dict()}")

    # ---- gráficos ----
    plots(c2)
    # ---- conclusões ----
    CONCLUSOES_MD.write_text(conclusoes(c2), encoding="utf-8")
    log(f"Conclusões: {CONCLUSOES_MD}")


def plots(df):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    cores = {"original": "#4C78A8", "ajustado": "#F58518"}

    def mean_tab(metric):
        return (df.groupby(["modelo", "condicao"])[metric].mean()
                  .unstack("condicao").reindex(MODELOS))

    def barras(metric, titulo, fname):
        if metric not in df.columns or df[metric].notna().sum() == 0:
            return
        t = mean_tab(metric).reindex(columns=[c for c in CONDICOES if c in df["condicao"].unique()])
        x = np.arange(len(t.index)); w = 0.38
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for k, cond in enumerate(t.columns):
            vals = t[cond].values
            bars = ax.bar(x + (k - 0.5) * w, vals, w, label=cond, color=cores.get(cond))
            for bb, val in zip(bars, vals):
                if not np.isnan(val):
                    ax.text(bb.get_x() + bb.get_width() / 2, val, f"{val:.2f}", ha="center", va="bottom", fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(t.index); ax.set_title(titulo)
        ax.set_ylabel(metric); ax.legend(title="condição"); ax.grid(axis="y", alpha=0.3)
        fig.tight_layout(); fig.savefig(PLOTS_DIR / fname, dpi=150); plt.close(fig)

    for met, nome, fn in [("lev_sim", "Similaridade Levenshtein (melhor de 3)", "barras_lev_sim.png"),
                          ("mos_principal", "MOS principal (melhor de 3)", "barras_mos.png"),
                          ("nisqa_overall", "NISQA overall", "barras_nisqa.png"),
                          ("dns_ovrl", "DNSMOS overall", "barras_dnsmos.png")]:
        barras(met, nome, fn)

    # delta ajustado - original
    mets = [m for m in ["lev_sim", "mos_principal", "nisqa_overall", "dns_ovrl"]
            if m in df.columns and df[m].notna().sum() > 0]
    if mets:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        x = np.arange(len(MODELOS)); w = 0.8 / max(1, len(mets))
        for j, m in enumerate(mets):
            t = mean_tab(m)
            if "ajustado" in t.columns and "original" in t.columns:
                d = (t["ajustado"] - t["original"]).reindex(MODELOS).values
                ax.bar(x + (j - (len(mets) - 1) / 2) * w, d, w, label=m)
        ax.axhline(0, color="k", lw=0.8); ax.set_xticks(x); ax.set_xticklabels(MODELOS)
        ax.set_title("Δ Ajustado − Original (positivo = ajustado melhor)")
        ax.set_ylabel("diferença de média"); ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
        fig.tight_layout(); fig.savefig(PLOTS_DIR / "delta_ajustado_vs_original.png", dpi=150); plt.close(fig)
    log(f"Gráficos em {PLOTS_DIR}")


def conclusoes(df):
    import numpy as np
    try:
        from scipy.stats import wilcoxon
    except Exception:
        wilcoxon = None
    L = ["# Conclusões preliminares — Original vs Ajustado", "",
         "Base: CSV2 (melhor das 3 repetições). Pareado por índice de sentença.",
         "Δ = média(ajustado) − média(original). **Δ > 0 ⇒ ajustado melhor**.", ""]
    mets = [m for m in ["lev_sim", "mos_principal", "nisqa_overall", "dns_ovrl"]
            if m in df.columns and df[m].notna().sum() > 0]
    for modelo in MODELOS:
        L += [f"## {modelo}", "", "| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |",
              "|---|---|---|---|---|---|"]
        sub = df[df.modelo == modelo]
        piv = sub.pivot_table(index="indice", columns="condicao", values=mets)
        for m in mets:
            try:
                o = piv[(m, "original")].astype(float).values
                a = piv[(m, "ajustado")].astype(float).values
            except KeyError:
                continue
            mo, ma = np.nanmean(o), np.nanmean(a); d = ma - mo
            p = float("nan")
            if wilcoxon is not None:
                mask = ~(np.isnan(a) | np.isnan(o))
                if mask.sum() >= 5 and not np.allclose(a[mask], o[mask]):
                    try:
                        p = wilcoxon(a[mask], o[mask]).pvalue
                    except Exception:
                        pass
            if np.isnan(p):
                leitura = "—"
            elif p < 0.05:
                leitura = "ajustado melhor*" if d > 0 else "degradou*"
            else:
                leitura = "sem diferença sig."
            ps = "n/d" if np.isnan(p) else f"{p:.3f}"
            L.append(f"| {m} | {mo:.3f} | {ma:.3f} | {d:+.3f} | {ps} | {leitura} |")
        L.append("")
    L += ["\\* p < 0,05.", "",
          "> Levenshtein menor no ajustado ⇒ perda de inteligibilidade; MOS menor ⇒ "
          "perda de qualidade. Δ≈0 e p≥0,05 ⇒ a adaptação de sotaque não degradou "
          "significativamente. Conclusões automáticas/preliminares; validação final = teste perceptivo humano."]
    return "\n".join(L)


# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="Experimento Final — métricas objetivas")
    ap.add_argument("--limit", type=int, default=0, help="processa só os N primeiros áudios (teste)")
    ap.add_argument("--overwrite", action="store_true", help="recalcula tudo")
    ap.add_argument("--only-agg", action="store_true", help="só refaz CSV2/gráficos a partir do CSV1")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--workers", type=int, default=5,
                    help="quantos áudios processar em paralelo (default 5). Cada processo carrega os modelos; reduza se faltar RAM.")
    args = ap.parse_args()
    if not args.only_agg:
        fase_metricas(args)
    fase_agregacao()
    log("=== Pipeline concluído ===")


if __name__ == "__main__":
    main()
