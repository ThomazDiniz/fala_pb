#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import subprocess
from pathlib import Path
from tqdm import tqdm
import pandas as pd

# Transcrição
from faster_whisper import WhisperModel

AUDIO_EXTS = {".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg", ".opus", ".wma", ".aiff", ".aif", ".alac"}

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return proc.returncode, out, err

def has_ffmpeg():
    return run(["ffmpeg", "-version"])[0] == 0 and run(["ffprobe", "-version"])[0] == 0

def ffprobe_duration(path):
    rc, out, err = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ])
    if rc == 0:
        try:
            return float(out.strip())
        except:
            return None
    return None

def discover_audios(raw_dir: Path):
    return sorted([p for p in raw_dir.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS])

def load_sidecar_texts(files):
    mapping = {}
    for p in files:
        txt = p.with_suffix(".txt")
        if txt.exists():
            try:
                mapping[p.stem] = txt.read_text(encoding="utf-8", errors="ignore").strip()
            except:
                mapping[p.stem] = txt.read_text(errors="ignore").strip()
    return mapping

def convert_audio(src: Path, dst: Path, sr: int, channels: int, bitdepth: int, normalize: bool):
    codec = "pcm_s24le" if bitdepth == 24 else "pcm_s16le"
    filters = []
    if normalize:
        # Normalização simples (1-pass) – pode deixar de fora se quiser áudio “cru”
        filters.append("loudnorm=I=-23:TP=-2:LRA=7")
    af = ",".join(filters) if filters else "anull"
    cmd = [
        "ffmpeg", "-nostdin", "-y",
        "-i", str(src),
        "-ac", str(channels),
        "-ar", str(sr),
        "-vn",
        "-af", af,
        "-c:a", codec,
        str(dst)
    ]
    rc, out, err = run(cmd)
    if rc != 0:
        raise RuntimeError(f"ffmpeg falhou: {src} -> {dst}\n{err}")

def transcribe(model: WhisperModel, wav_path: Path, language: str, beam_size: int, vad: bool, temperature: float):
    """
    Retorna texto transcrito. Usa VAD e beam search configuráveis.
    """
    segments, info = model.transcribe(
        str(wav_path),
        language=language,                # "pt" para PT-BR; use None para autodetect
        beam_size=beam_size,
        vad_filter=vad,
        vad_parameters=dict(min_silence_duration_ms=200),
        temperature=temperature
    )
    # Concatena segmentos com espaço; se quiser timestamps, dá pra salvar também
    text = " ".join(seg.text.strip() for seg in segments if seg.text)
    return text.strip()

def main():
    ap = argparse.ArgumentParser(description="Prepara dataset de áudio (converte, renomeia) e transcreve (Whisper).")
    ap.add_argument("--raw", default="raw", type=str, help="Pasta com áudios brutos")
    ap.add_argument("--out", default="data", type=str, help="Pasta para áudios convertidos")
    ap.add_argument("--metadata", default="metadata.csv", type=str, help="Arquivo CSV de saída na raiz")
    ap.add_argument("--sr", default=22050, type=int, help="Sample rate alvo (ex.: 16000, 22050, 24000)")
    ap.add_argument("--channels", default=1, type=int, choices=[1,2], help="Canais (1=mono, 2=stereo)")
    ap.add_argument("--bitdepth", default=16, type=int, choices=[16,24], help="Profundidade de bits PCM")
    ap.add_argument("--normalize", action="store_true", help="Normalizar loudness (EBU R128 simples)")
    ap.add_argument("--start-index", default=1, type=int, help="Índice inicial para 1.wav, 2.wav, ...")
    ap.add_argument("--whisper-model", default="small", type=str,
                    help="Modelo Faster-Whisper (ex.: tiny, base, small, medium, large-v3)")
    ap.add_argument("--device", default="cpu", choices=["cpu", "cuda"], help="Dispositivo para transcrição")
    ap.add_argument("--compute-type", default="int8", type=str,
                    help="Tipo de precisão (cpu: int8/int8_float16; gpu: float16/float32)")
    ap.add_argument("--language", default="pt", type=str,
                    help="Código de idioma (ex.: pt). Use 'auto' para autodetect")
    ap.add_argument("--beam-size", default=5, type=int, help="Beam size para decodificação")
    ap.add_argument("--no-vad", action="store_true", help="Desativa VAD (detecção de voz)")
    ap.add_argument("--temperature", default=0.0, type=float, help="Temperatura de decodificação (0.0 a 1.0)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Se existir data/N.wav e .txt com mesmo ID, pula transcrição/conversão")
    args = ap.parse_args()

    raw_dir = Path(args.raw).resolve()
    out_dir = Path(args.out).resolve()
    meta_path = Path(args.metadata).resolve()

    if not raw_dir.exists():
        print(f"ERRO: pasta raw não encontrada: {raw_dir}", file=sys.stderr)
        sys.exit(1)

    if not has_ffmpeg():
        print("ERRO: ffmpeg/ffprobe não encontrados no PATH.", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    files = discover_audios(raw_dir)
    if not files:
        print("Nenhum arquivo de áudio encontrado em 'raw/'.", file=sys.stderr)
        sys.exit(1)

    # Sidecar .txt (caso já existam transcrições manuais)
    sidecar = load_sidecar_texts(files)

    # Carrega modelo Whisper
    lang = None if args.language.lower() == "auto" else args.language
    model = WhisperModel(args.whisper-model if hasattr(args, "whisper-model") else args.whisper_model,
                         device=args.device, compute_type=args.compute_type)

    rows = []
    idx = args.start_index

    for src in tqdm(files, desc="Processando"):
        dst_wav = out_dir / f"{idx}.wav"
        txt_out = out_dir / f"{idx}.txt"  # cache da transcrição

        if args.skip_existing and dst_wav.exists() and txt_out.exists():
            duration = ffprobe_duration(dst_wav)
            text = txt_out.read_text(encoding="utf-8", errors="ignore").strip()
            rows.append({
                "id": idx,
                "path": str(dst_wav.relative_to(out_dir.parent if out_dir.parent.exists() else Path.cwd())),
                "duration_sec": round(duration, 6) if duration is not None else None,
                "sample_rate": args.sr, "channels": args.channels, "bit_depth": args.bitdepth,
                "original_path": str(src), "original_name": src.name, "text": text
            })
            idx += 1
            continue

        # Converter para WAV padronizado
        try:
            convert_audio(src, dst_wav, sr=args.sr, channels=args.channels, bitdepth=args.bitdepth, normalize=args.normalize)
        except Exception as e:
            print(f"[ERRO] Conversão falhou para {src.name}: {e}", file=sys.stderr)
            continue

        duration = ffprobe_duration(dst_wav)

        # Texto: prioridade lado a lado (.txt do arquivo original) > transcrição Whisper
        text = sidecar.get(src.stem, "")
        if not text:
            try:
                text = transcribe(
                    model=model,
                    wav_path=dst_wav,
                    language=lang,
                    beam_size=args.beam_size,
                    vad=(not args.no_vad),
                    temperature=args.temperature
                )
            except Exception as e:
                print(f"[ERRO] Transcrição falhou para {dst_wav.name}: {e}", file=sys.stderr)
                text = ""

        # Salva um cache .txt por arquivo convertido (útil para revisões manuais)
        try:
            txt_out.write_text(text, encoding="utf-8")
        except Exception as e:
            print(f"[AVISO] Não foi possível salvar {txt_out.name}: {e}", file=sys.stderr)

        rows.append({
            "id": idx,
            "path": str(dst_wav.relative_to(out_dir.parent if out_dir.parent.exists() else Path.cwd())),
            "duration_sec": round(duration, 6) if duration is not None else None,
            "sample_rate": args.sr,
            "channels": args.channels,
            "bit_depth": args.bitdepth,
            "original_path": str(src),
            "original_name": src.name,
            "text": text
        })
        idx += 1

    if not rows:
        print("Nenhum arquivo foi processado com sucesso.", file=sys.stderr)
        sys.exit(2)

    df = pd.DataFrame(rows, columns=[
        "id", "path", "duration_sec", "sample_rate", "channels", "bit_depth",
        "original_path", "original_name", "text"
    ])
    df.to_csv(meta_path, index=False, quoting=csv.QUOTE_MINIMAL)

    print(f"OK! Convertidos e transcritos: {len(rows)} áudios")
    print(f"Saída de áudio: {out_dir}")
    print(f"Metadata: {meta_path}")

if __name__ == "__main__":
    main()
