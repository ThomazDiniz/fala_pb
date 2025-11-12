#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Avaliação em lote para pastas dentro de "inferências".
Para cada subpasta, encontra pares áudio + texto, calcula NISQA, DNSMOS, faz transcrição
com Whisper e mede Levenshtein. Gera um CSV agregando tudo (sem gráficos automáticos).

Requisitos principais:
  pip install torch torchaudio torchmetrics openai-whisper tqdm pandas

Estrutura esperada:
  inferências/
    modelo_A/
      exemplo1.wav
      exemplo1.txt
      ...
    modelo_B/
      ...

Saídas:
  resultados/
    avaliacao.csv
    logs.txt

Observação: DNSMOS e NISQA do torchmetrics podem baixar pesos no primeiro uso.
"""

from __future__ import annotations

import sys
import re
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

import torch
import torchaudio
import pandas as pd
from tqdm import tqdm
import whisper

from torchmetrics.functional.audio.nisqa import non_intrusive_speech_quality_assessment as tm_nisqa
from torchmetrics.audio.dnsmos import DeepNoiseSuppressionMeanOpinionScore

INFERENCIAS_DIR = Path("inferências")
RESULTS_DIR = Path("resultados")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_EXTS = {
    ".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg", ".opus", ".wma", ".aiff", ".aif", ".alac"
}

WHISPER_MODEL = "small"
WHISPER_LANGUAGE = "pt"
USE_FP16 = False

CSV_PATH = RESULTS_DIR / "avaliacao.csv"
LOG_PATH = RESULTS_DIR / "logs.txt"


def log(msg: str, *, also_print: bool = True):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(msg.rstrip() + "\n")
    if also_print:
        print(msg)


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


def load_audio_mono16k(path: Path) -> Tuple[torch.Tensor, int, float]:
    wav, sr = torchaudio.load(str(path))
    if wav.dim() == 2 and wav.shape[0] > 1:
        wav = wav.mean(0, keepdim=True)
    elif wav.dim() == 1:
        wav = wav.unsqueeze(0)
    if sr != 16000:
        wav = torchaudio.functional.resample(wav, sr, 16000)
        sr = 16000
    dur = wav.shape[-1] / float(sr)
    return wav, sr, dur


def compute_nisqa(wav_mono_16k: torch.Tensor, sr: int):
    scores = tm_nisqa(wav_mono_16k.squeeze(0), fs=sr)
    return tuple(float(x) for x in scores.tolist())


def compute_dnsmos(wav_mono_16k: torch.Tensor, sr: int):
    metric = DeepNoiseSuppressionMeanOpinionScore(fs=sr, personalized=False)
    out = metric(wav_mono_16k.squeeze(0))
    dns_sig = dns_bak = dns_ovrl = dns_ovrl_alt = None
    if isinstance(out, (list, tuple, torch.Tensor)):
        vals = out if not torch.is_tensor(out) else out.flatten().tolist()
        if len(vals) >= 3:
            dns_sig, dns_bak, dns_ovrl = [float(vals[i]) for i in range(3)]
            if len(vals) > 3:
                dns_ovrl_alt = float(vals[3])
    else:
        raise RuntimeError(f"Saída inesperada do DNSMOS: {out}")
    return dns_sig, dns_bak, dns_ovrl, dns_ovrl_alt


def transcribe(model: whisper.Whisper, audio_path: Path, language: str, fp16: bool) -> str:
    result = model.transcribe(str(audio_path), language=language, fp16=fp16)
    return result.get("text", "").strip()


@dataclass
class Row:
    model: str
    rel_path: str
    file: str
    duration_sec: float
    nisqa_overall: Optional[float]
    nisqa_noisiness: Optional[float]
    nisqa_discontinuity: Optional[float]
    nisqa_coloration: Optional[float]
    nisqa_loudness: Optional[float]
    dns_sig: Optional[float]
    dns_bak: Optional[float]
    dns_ovrl: Optional[float]
    dns_ovrl_alt: Optional[float]
    lev_dist: Optional[int]
    lev_norm: Optional[float]
    ref_chars: Optional[int]
    texto: str
    texto_delta: str


def find_pairs(base_dir: Path):
    pairs = []
    for audio_path in base_dir.rglob("*"):
        if audio_path.suffix.lower() in AUDIO_EXTS and audio_path.is_file():
            txt_path = audio_path.with_suffix(".txt")
            if not txt_path.exists():
                candidates = list(audio_path.parent.glob(f"{audio_path.stem}.txt"))
                if candidates:
                    txt_path = candidates[0]
            if txt_path.exists():
                pairs.append((audio_path, txt_path))
            else:
                log(f"[AVISO] Texto não encontrado para {audio_path}", also_print=False)
    return sorted(pairs, key=lambda x: str(x[0]))


def main():
    if not INFERENCIAS_DIR.exists():
        log(f"Pasta não encontrada: {INFERENCIAS_DIR}")
        sys.exit(1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"Usando dispositivo: {device}")

    log(f"Carregando Whisper: {WHISPER_MODEL}")
    model_whisper = whisper.load_model(WHISPER_MODEL, device=device)

    rows: List[Row] = []

    subdirs = sorted([p for p in INFERENCIAS_DIR.iterdir() if p.is_dir()])
    if not subdirs:
        log("Nenhuma subpasta encontrada dentro de inferências")
        sys.exit(1)

    for sub in subdirs:
        model_name = sub.name
        log(f"Processando modelo: {model_name}")
        pairs = find_pairs(sub)
        if not pairs:
            log(f"Nenhum par áudio+texto em {sub}")
            continue

        for audio_path, text_path in tqdm(pairs, desc=f"{model_name}"):
            try:
                wav, sr, dur = load_audio_mono16k(audio_path)

                nisqa_overall = nisqa_noisiness = nisqa_discontinuity = None
                nisqa_coloration = nisqa_loudness = None
                dns_sig = dns_bak = dns_ovrl = dns_ovrl_alt = None
                lev_dist = lev_norm = ref_len = None

                try:
                    nisqa_overall, nisqa_noisiness, nisqa_discontinuity, nisqa_coloration, nisqa_loudness = compute_nisqa(wav, sr)
                except Exception as e:
                    log(f"[NISQA ERRO] {audio_path}: {e}", also_print=False)

                try:
                    dns_sig, dns_bak, dns_ovrl, dns_ovrl_alt = compute_dnsmos(wav, sr)
                except Exception as e:
                    log(f"[DNSMOS ERRO] {audio_path}: {e}", also_print=False)

                hyp_raw = transcribe(model_whisper, audio_path, WHISPER_LANGUAGE, USE_FP16)
                ref_raw = text_path.read_text(encoding="utf-8").strip()

                ref = normalize_text(ref_raw)
                hyp = normalize_text(hyp_raw)
                ref_len = len(ref)
                lev_dist = levenshtein(ref, hyp)
                lev_norm = lev_dist / max(1, ref_len)

                rows.append(
                    Row(
                        model=model_name,
                        rel_path=str(audio_path.relative_to(INFERENCIAS_DIR)),
                        file=audio_path.name,
                        duration_sec=float(dur),
                        nisqa_overall=nisqa_overall,
                        nisqa_noisiness=nisqa_noisiness,
                        nisqa_discontinuity=nisqa_discontinuity,
                        nisqa_coloration=nisqa_coloration,
                        nisqa_loudness=nisqa_loudness,
                        dns_sig=dns_sig,
                        dns_bak=dns_bak,
                        dns_ovrl=dns_ovrl,
                        dns_ovrl_alt=dns_ovrl_alt,
                        lev_dist=lev_dist,
                        lev_norm=lev_norm,
                        ref_chars=ref_len,
                        texto=ref_raw,
                        texto_delta=hyp_raw,
                    )
                )

            except Exception as e:
                log(f"[ERRO] {audio_path}: {e}")
                log(traceback.format_exc(), also_print=False)
                continue

    if not rows:
        log("Nenhum resultado gerado. Encerrando.")
        return

    df = pd.DataFrame([asdict(r) for r in rows])
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    log(f"CSV salvo em: {CSV_PATH.resolve()}")


if __name__ == "__main__":
    main()
