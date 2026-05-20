#!/usr/bin/env python3
"""Plot F5-TTS training loss by step and epoch (style aligned with plot_xtts_training_loss.py)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "docs" / "15" / "f5tts"
OUT_DIR = DATA_DIR / "outputs"

STEP_CSV = DATA_DIR / "loss_by_step.csv"
EPOCH_CSV = DATA_DIR / "loss_by_epoch.csv"
EPOCH_TIMING_CSV = DATA_DIR / "epoch_timing.csv"

TITLE_STEP = "Gráfico de perda do ajuste fino do F5-TTS por passo de treino"
TITLE_EPOCH = "Gráfico de perda do ajuste fino do F5-TTS por época"
TITLE_COMBINED = "Gráfico de perda do ajuste fino do F5-TTS"

COLOR = "#1f4e79"


def load_step_data() -> pd.DataFrame:
    df = pd.read_csv(STEP_CSV)
    if "global_step" not in df.columns or "loss" not in df.columns:
        raise RuntimeError(f"Expected global_step, loss columns in {STEP_CSV}")
    df = df.sort_values("global_step").reset_index(drop=True)

    if EPOCH_TIMING_CSV.exists():
        timing = pd.read_csv(EPOCH_TIMING_CSV)
        boundaries = timing["global_step_end"].tolist()
        batches_per_epoch = int(timing["batches_in_epoch"].iloc[0])
    else:
        batches_per_epoch = 17642
        boundaries = [batches_per_epoch * (i + 1) for i in range(3)]

    def step_to_epoch(step: int) -> int:
        for i, end in enumerate(boundaries):
            if step <= end:
                return i
        return len(boundaries) - 1

    df["epoch"] = df["global_step"].map(step_to_epoch)
    return df


def epoch_means_from_steps(df: pd.DataFrame) -> pd.DataFrame:
    epoch_df = (
        df.groupby("epoch", as_index=False)["loss"]
        .mean()
        .rename(columns={"loss": "mean_loss"})
    )
    epoch_df["epoch_display"] = epoch_df["epoch"] + 1
    return epoch_df


def plot_loss_by_step(df: pd.DataFrame, out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=120)
    ax.plot(df["global_step"], df["loss"], color=COLOR, linewidth=0.55, alpha=0.85)
    ax.set_xlabel("Passo global de treino")
    ax.set_ylabel("Perda de Treino")
    ax.set_title(TITLE_STEP, fontsize=11, pad=12)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def plot_loss_by_epoch(epoch_df: pd.DataFrame, out_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.plot(
        epoch_df["epoch_display"],
        epoch_df["mean_loss"],
        marker="o",
        color=COLOR,
        linewidth=1.5,
    )
    ax.set_xlabel("Época")
    ax.set_ylabel("Perda de Treino")
    ax.set_title(TITLE_EPOCH, fontsize=11, pad=12)
    ax.set_xticks(epoch_df["epoch_display"])
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def plot_combined(df: pd.DataFrame, epoch_df: pd.DataFrame, out_png: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), dpi=120, sharex=False)
    axes[0].plot(df["global_step"], df["loss"], color=COLOR, linewidth=0.55, alpha=0.85)
    axes[0].set_ylabel("Perda de Treino")
    axes[0].set_xlabel("Passo global de treino")
    axes[0].set_title("Por passo de treino", fontsize=10)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        epoch_df["epoch_display"],
        epoch_df["mean_loss"],
        marker="o",
        color=COLOR,
        linewidth=1.5,
    )
    axes[1].set_ylabel("Perda de Treino")
    axes[1].set_xlabel("Época")
    axes[1].set_title("Por época", fontsize=10)
    axes[1].set_xticks(epoch_df["epoch_display"])
    axes[1].grid(True, alpha=0.3)

    fig.suptitle(TITLE_COMBINED, fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_step_data()
    epoch_df = epoch_means_from_steps(df)

    df[["global_step", "epoch", "loss"]].to_csv(
        OUT_DIR / "training_loss_by_step.csv", index=False
    )
    epoch_df.to_csv(OUT_DIR / "training_loss_by_epoch.csv", index=False)

    plot_loss_by_step(df, OUT_DIR / "training_loss_by_step.png")
    plot_loss_by_step(df, OUT_DIR / "grafico_perda_ajuste_fino_f5tts_por_passo.png")
    plot_loss_by_epoch(epoch_df, OUT_DIR / "training_loss_by_epoch.png")
    plot_loss_by_epoch(epoch_df, OUT_DIR / "grafico_perda_ajuste_fino_f5tts_por_epoca.png")
    plot_combined(df, epoch_df, OUT_DIR / "training_loss_step_and_epoch.png")

    # Legacy paths at f5tts/ root (site embeds)
    plot_loss_by_step(df, DATA_DIR / "loss.png")
    plot_loss_by_epoch(epoch_df, DATA_DIR / "loss_by_epoch.png")

    print(f"Parsed {len(df)} train loss points, epochs {df['epoch'].min()}-{df['epoch'].max()}")
    print(f"Wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
