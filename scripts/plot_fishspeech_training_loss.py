#!/usr/bin/env python3
"""Plot Fish Speech training loss by step (style aligned with XTTS/F5/Orpheus plots)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "docs" / "17" / "fishspeech"
OUT_DIR = DATA_DIR / "outputs"

STEP_CSV = DATA_DIR / "train_loss_by_step.csv"

TITLE_STEP = "Gráfico de perda do ajuste fino do Fish Speech por passo de treino"

COLOR = "#1f4e79"


def load_step_data() -> pd.DataFrame:
    df = pd.read_csv(STEP_CSV)
    step_col = "global_step" if "global_step" in df.columns else "step"
    if step_col not in df.columns or "loss" not in df.columns:
        raise RuntimeError(f"Expected step and loss columns in {STEP_CSV}")
    out = (
        df[[step_col, "loss"]]
        .rename(columns={step_col: "global_step"})
        .sort_values("global_step")
        .reset_index(drop=True)
    )
    return out


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_step_data()

    export = df[["global_step", "loss"]].copy()
    export.to_csv(OUT_DIR / "training_loss_by_step.csv", index=False)
    export.to_csv(DATA_DIR / "train_loss_by_step.csv", index=False)

    plot_loss_by_step(df, OUT_DIR / "training_loss_by_step.png")
    plot_loss_by_step(df, OUT_DIR / "grafico_perda_ajuste_fino_fishspeech_por_passo.png")
    plot_loss_by_step(df, DATA_DIR / "train_loss_by_step.png")

    print(f"Parsed {len(df)} train loss points")
    print(f"Steps {df['global_step'].min()}–{df['global_step'].max()}")
    print(f"Loss min/mean/max: {df['loss'].min():.4f} / {df['loss'].mean():.4f} / {df['loss'].max():.4f}")
    print(f"Wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
