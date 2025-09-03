# prepare_csv_wavs.py
import argparse, os, json, unicodedata, sys
from typing import List, Tuple

import pandas as pd
import soundfile as sf
import librosa
import pyarrow as pa
import pyarrow.ipc as pa_ipc

def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)

def read_metadata(input_dir: str) -> pd.DataFrame:
    meta = os.path.join(input_dir, "metadata.csv")
    if not os.path.isfile(meta):
        print(f"[ERRO] metadata.csv não encontrado em: {input_dir}")
        sys.exit(1)
    try:
        df = pd.read_csv(meta, sep="|", dtype={"audio": str, "text": str})
    except Exception as e:
        print(f"[ERRO] Falha lendo metadata.csv: {e}")
        sys.exit(1)
    if "audio" not in df.columns or "text" not in df.columns:
        print("[ERRO] metadata.csv deve possuir cabeçalho 'audio|text'")
        sys.exit(1)
    # Normaliza texto (UTF-8 + NFC) e troca pipes no texto
    df["text"] = df["text"].fillna("").map(lambda t: nfc(str(t)).replace("|", ",").strip())
    df["audio"] = df["audio"].fillna("").map(lambda p: str(p).replace("\\", "/").strip())
    return df

def validate_and_durations(base_dir: str, rel_paths: List[str], sr_target: int) -> Tuple[List[str], List[float], List[str]]:
    abs_paths, durs, warns = [], [], []
    for rel in rel_paths:
        rel_norm = rel.replace("\\", "/")
        abs_path = os.path.join(base_dir, rel_norm)
        abs_paths.append(abs_path)
        if not os.path.isfile(abs_path):
            warns.append(f"ARQUIVO AUSENTE: {rel_norm}")
            durs.append(0.0)
            continue
        try:
            info = sf.info(abs_path)
            if info.samplerate != sr_target:
                warns.append(f"SR DIFERENTE ({info.samplerate}!={sr_target}): {rel_norm}")
            if info.channels != 1:
                warns.append(f"NAO MONO (channels={info.channels}): {rel_norm}")
            dur = float(librosa.get_duration(path=abs_path))
        except Exception as e:
            warns.append(f"ERRO AO LER {rel_norm}: {e}")
            dur = 0.0
        durs.append(dur)
    return abs_paths, durs, warns

def build_vocab(texts: List[str]) -> List[str]:
    charset = set()
    for t in texts:
        for ch in str(t):
            charset.add(ch)
    return sorted(charset)

def save_duration_json(out_dir: str, rel_audio: List[str], durs: List[float]):
    os.makedirs(out_dir, exist_ok=True)
    mapping = { rel_audio[i]: float(durs[i]) for i in range(len(rel_audio)) }
    with open(os.path.join(out_dir, "duration.json"), "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

def save_vocab(out_dir: str, vocab: List[str]):
    with open(os.path.join(out_dir, "vocab.txt"), "w", encoding="utf-8") as f:
        for ch in vocab:
            f.write(f"{ch}\n")

def save_raw_arrow(out_dir: str, rel_audio: List[str], texts: List[str]):
    table = pa.table({"audio": rel_audio, "text": texts})
    arrow_path = os.path.join(out_dir, "raw.arrow")
    with pa_ipc.new_file(arrow_path, table.schema) as writer:
        writer.write_table(table)

def main():
    ap = argparse.ArgumentParser(
        description="Prepara dataset (raw.arrow, duration.json, vocab.txt) para F5-TTS a partir de metadata.csv (audio|text)."
    )
    ap.add_argument("input_dir", help="Pasta com metadata.csv e subpasta de áudios")
    ap.add_argument("output_dir", help="Pasta de saída (ex: data/ptbr_char)")
    ap.add_argument("--audio-subdir", default=None,
                    help="Força subpasta de áudio (ex: wavs24). Se omitido, usa a do metadata.")
    ap.add_argument("--sr", type=int, default=24000, help="Sample rate esperado (default: 24000)")
    args = ap.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)
    sr = args.sr

    df = read_metadata(input_dir)

    # Aponta para a subpasta correta (ex: wavs24) mantendo apenas nome base + .wav
    if args.audio_subdir:
        def _force_dir(p):
            base = os.path.splitext(os.path.basename(p))[0] + ".wav"
            return f"{args.audio_subdir.strip().replace('\\','/')}/{base}"
        rel_audio = df["audio"].map(_force_dir).tolist()
    else:
        # Usa o caminho do metadata como está (já deve referenciar wavs24/ ou wavs/)
        rel_audio = df["audio"].tolist()

    texts = df["text"].tolist()

    abs_audio, durs, warns = validate_and_durations(input_dir, rel_audio, sr)

    ok = sum(1 for d in durs if d > 0)
    print(f"Linhas no metadata: {len(rel_audio)}")
    print(f"Lidas com sucesso : {ok}")
    if warns:
        print("\nAvisos/Erros:")
        for w in warns[:40]:
            print(" -", w)
        if len(warns) > 40:
            print(f"... (+{len(warns)-40} avisos)")

    os.makedirs(output_dir, exist_ok=True)
    save_duration_json(output_dir, rel_audio, durs)

    vocab = build_vocab(texts)
    save_vocab(output_dir, vocab)

    save_raw_arrow(output_dir, rel_audio, texts)

    total_sec = sum(durs)
    print("\n=== RESUMO ===")
    print(f"Saída: {output_dir}")
    print(f"- raw.arrow       OK")
    print(f"- duration.json   OK")
    print(f"- vocab.txt       OK (chars={len(vocab)})")
    print(f"Duração total (h): {total_sec/3600:.2f}")

if __name__ == "__main__":
    main()
