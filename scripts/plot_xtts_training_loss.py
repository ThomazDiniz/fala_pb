#!/usr/bin/env python3
"""Parse XTTS trainer_0_log.txt and plot train loss (no eval) by step and epoch."""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "docs" / "15" / "xtts" / "trainer_0_log.txt"
OUT_DIR = ROOT / "docs" / "15" / "xtts" / "outputs"

TITLE_STEP = "Gráfico de perda do ajuste fino do XTTS por passo de treino"
TITLE_EPOCH = "Gráfico de perda do ajuste fino do XTTS por época"
TITLE_COMBINED = "Gráfico de perda do ajuste fino do XTTS"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
GLOBAL_STEP_RE = re.compile(r"GLOBAL_STEP:\s*(\d+)")
EPOCH_RE = re.compile(r"EPOCH:\s*(\d+)\s*/\s*(\d+)")
LOSS_RE = re.compile(r"\|\s*>\s*loss:\s*([0-9.eE+-]+)\s+\(([0-9.eE+-]+)\)")


def strip_ansi(line: str) -> str:
    return ANSI_RE.sub("", line).strip()


def parse_trainer_log(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    current_epoch = 0
    in_eval = False
    pending_step: int | None = None

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = strip_ansi(raw)
        if not line:
            continue

        if line.startswith("> EVALUATION"):
            in_eval = True
            pending_step = None
            continue

        m_epoch = EPOCH_RE.search(line)
        if m_epoch:
            current_epoch = int(m_epoch.group(1))
            in_eval = False
            pending_step = None
            continue

        if in_eval:
            continue

        m_step = GLOBAL_STEP_RE.search(line)
        if m_step:
            pending_step = int(m_step.group(1))
            continue

        m_loss = LOSS_RE.search(line)
        if m_loss and pending_step is not None:
            instant = float(m_loss.group(1))
            running = float(m_loss.group(2))
            rows.append(
                {
                    "global_step": pending_step,
                    "epoch": current_epoch,
                    "loss": instant,
                    "loss_running_avg": running,
                }
            )
            pending_step = None

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No training loss rows parsed from {path}")
    return df.sort_values("global_step").reset_index(drop=True)


def plot_loss_by_step(df: pd.DataFrame, out_png: Path) -> None:
    # Valor instantâneo por passo (1º número no log), não a média móvel entre parênteses.
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=120)
    ax.plot(df["global_step"], df["loss"], color="#1f4e79", linewidth=0.55, alpha=0.85)
    ax.set_xlabel("Passo global de treino")
    ax.set_ylabel("Perda de Treino")
    ax.set_title(TITLE_STEP, fontsize=11, pad=12)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def plot_loss_by_epoch(df: pd.DataFrame, out_png: Path) -> None:
    epoch_df = (
        df.groupby("epoch", as_index=False)["loss"]
        .mean()
        .rename(columns={"loss": "mean_loss"})
    )
    epoch_df["epoch_display"] = epoch_df["epoch"] + 1

    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.plot(
        epoch_df["epoch_display"],
        epoch_df["mean_loss"],
        marker="o",
        color="#1f4e79",
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
    return epoch_df


def plot_combined(df: pd.DataFrame, epoch_df: pd.DataFrame, out_png: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), dpi=120, sharex=False)
    axes[0].plot(df["global_step"], df["loss"], color="#1f4e79", linewidth=0.55, alpha=0.85)
    axes[0].set_ylabel("Perda de Treino")
    axes[0].set_xlabel("Passo global de treino")
    axes[0].set_title("Por passo de treino", fontsize=10)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(
        epoch_df["epoch_display"],
        epoch_df["mean_loss"],
        marker="o",
        color="#1f4e79",
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
    df = parse_trainer_log(LOG_PATH)

    df.to_csv(OUT_DIR / "training_loss_by_step.csv", index=False)
    epoch_df = (
        df.groupby("epoch", as_index=False)["loss"]
        .mean()
        .rename(columns={"loss": "mean_loss"})
    )
    epoch_df["epoch_display"] = epoch_df["epoch"] + 1
    epoch_df.to_csv(OUT_DIR / "training_loss_by_epoch.csv", index=False)

    plot_loss_by_step(df, OUT_DIR / "training_loss_by_step.png")
    plot_loss_by_step(df, OUT_DIR / "grafico_perda_ajuste_fino_xtts_por_passo.png")
    epoch_df = plot_loss_by_epoch(df, OUT_DIR / "training_loss_by_epoch.png")
    plot_loss_by_epoch(df, OUT_DIR / "grafico_perda_ajuste_fino_xtts_por_epoca.png")
    plot_combined(df, epoch_df, OUT_DIR / "training_loss_step_and_epoch.png")

    print(f"Parsed {len(df)} train loss points, epochs {df['epoch'].min()}-{df['epoch'].max()}")
    print(f"Wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
