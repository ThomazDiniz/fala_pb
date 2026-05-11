#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera figuras PNG (forma de onda linear, espectrograma STFT linear, Mel) em dataset/outputs/.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    import librosa
    import librosa.display
except ImportError:
    librosa = None


def default_audio_candidates(dataset_root: Path) -> list[Path]:
    data_dir = dataset_root / "data"
    return sorted(data_dir.glob("*.wav")) if data_dir.exists() else []


def synthesize_demo(sr: int, duration_sec: float) -> tuple[np.ndarray, int]:
    """Sinal sintético (multi‑tom + ruído) quando não há WAV disponível."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    y = 0.2 * np.sin(2 * np.pi * 220 * t)
    y += 0.15 * np.sin(2 * np.pi * 440 * t + 1.3)
    y += 0.1 * np.sin(2 * np.pi * 880 * (t + 0.02 * np.sin(2 * np.pi * 3 * t)))
    y += 0.02 * np.random.default_rng(42).standard_normal(len(t)).astype(np.float64)
    y = np.clip(y, -1.0, 1.0)
    return y.astype(np.float32), sr


def load_audio(path: Path | None, sr_hint: int) -> tuple[np.ndarray, int]:
    if path is None or not path.exists():
        return synthesize_demo(sr_hint, duration_sec=2.8)
    if librosa is None:
        raise RuntimeError("librosa é necessário para carregar arquivos de áudio.")
    y, sr = librosa.load(str(path), sr=None, mono=True)
    return y.astype(np.float32), int(sr)


def plot_waveform_linear(y: np.ndarray, sr: int, out_path: Path) -> None:
    t = np.arange(len(y)) / float(sr)
    fig, ax = plt.subplots(figsize=(10, 3), dpi=120)
    ax.plot(t, y, color="#1f4e79", linewidth=0.35)
    ax.set_title("Forma de onda — amplitude em escala linear")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(0, t[-1] if len(t) else 1)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def plot_spectrogram_linear(y: np.ndarray, sr: int, out_path: Path, n_fft: int, hop: int) -> None:
    if librosa is None:
        raise RuntimeError("librosa é necessário para o espectrograma.")
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop, center=True))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    img = librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=hop,
        x_axis="time",
        y_axis="linear",
        ax=ax,
        cmap="magma",
    )
    ax.set_title("Espectrograma — frequência em escala linear (STFT)")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Frequência (Hz)")
    fig.colorbar(img, ax=ax, format="%+2.0f dB", label="Potência (dB)")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def plot_mel_spectrogram(y: np.ndarray, sr: int, out_path: Path, n_fft: int, hop: int, n_mels: int) -> None:
    if librosa is None:
        raise RuntimeError("librosa é necessário para o espectrograma Mel.")
    S = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop,
        n_mels=n_mels,
        power=2.0,
    )
    S_db = librosa.power_to_db(S, ref=np.max)
    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    img = librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=hop,
        x_axis="time",
        y_axis="mel",
        ax=ax,
        cmap="magma",
    )
    ax.set_title("Espectrograma Mel — perceptualmente espaçado (escala Mel)")
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Frequência Mel")
    fig.colorbar(img, ax=ax, format="%+2.0f dB", label="Potência (dB)")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description="Exporta PNGs da forma de onda e dos espectrogramas.")
    ap.add_argument(
        "--audio",
        type=str,
        default=None,
        help="Caminho para .wav/.mp3 (opcional). Se omitido e pasta data/ existir, usa o primeiro WAV.",
    )
    ap.add_argument(
        "--out",
        type=str,
        default=None,
        help="Pasta de saída (padrão: dataset/outputs relativo a este script).",
    )
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    out_dir = Path(args.out).resolve() if args.out else (here / "outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates = default_audio_candidates(here)
    audio_path = Path(args.audio).resolve() if args.audio else (candidates[0] if candidates else None)

    if librosa is None:
        print("Instale librosa para carregar WAV reais ou use apenas modo demo com numpy não está implementado aqui.")
        sys.exit(1)

    sr_default = 22050
    y, sr = load_audio(audio_path, sr_default)

    n_fft = 1024
    hop = 256

    suffix = ""
    stem = "_demo"
    if audio_path and audio_path.exists():
        stem = audio_path.stem
        suffix = f"_{stem}"

    wf_name = out_dir / f"forma_de_onda_linear{suffix}.png"
    spec_name = out_dir / f"espectrograma_linear{suffix}.png"
    mel_name = out_dir / f"espectrograma_mel{suffix}.png"

    plot_waveform_linear(y, sr, wf_name)
    plot_spectrogram_linear(y, sr, spec_name, n_fft=n_fft, hop=hop)
    plot_mel_spectrogram(y, sr, mel_name, n_fft=n_fft, hop=hop, n_mels=128)

    src = str(audio_path) if audio_path and audio_path.exists() else "(sinal sintético — sem WAV em data/)"
    print("OK")
    print(f"  Fonte: {src}")
    print(f"  {wf_name}")
    print(f"  {spec_name}")
    print(f"  {mel_name}")


if __name__ == "__main__":
    main()
