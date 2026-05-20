#!/usr/bin/env python3
"""Plot Orpheus/Unsloth (artoodtoo_ft_e3) training loss by step and epoch (XTTS/F5 style)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "docs" / "15" / "artoodtoo_ft_e3"
OUT_DIR = DATA_DIR / "outputs"

STEP_CSV = DATA_DIR / "loss_by_step.csv"
LEGACY_PNG = DATA_DIR / "loss_curve_by_step.png"  # original chart (train + eval legend)
TRAINING_STATS_JSON = DATA_DIR / "training_stats.json"
TRAINER_STATE_JSON = DATA_DIR / "trainer_state.json"
TRAINING_REPORT = DATA_DIR / "training_report.txt"

TITLE_STEP = "Gráfico de perda do ajuste fino do Orpheus por passo de treino"
TITLE_EPOCH = "Gráfico de perda do ajuste fino do Orpheus por época"
TITLE_COMBINED = "Gráfico de perda do ajuste fino do Orpheus"

COLOR = "#1f4e79"


def _read_global_steps_cap() -> int:
    if TRAINING_REPORT.exists():
        m = re.search(r"global_steps:\s*(\d+)", TRAINING_REPORT.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1))
    return 3351


def load_from_csv() -> pd.DataFrame | None:
    if not STEP_CSV.exists():
        return None
    df = pd.read_csv(STEP_CSV)
    if "global_step" not in df.columns or "loss" not in df.columns:
        raise RuntimeError(f"Expected global_step, loss in {STEP_CSV}")
    return df.sort_values("global_step").reset_index(drop=True)


def load_from_training_stats_json() -> pd.DataFrame | None:
    if not TRAINING_STATS_JSON.exists():
        return None
    data = json.loads(TRAINING_STATS_JSON.read_text(encoding="utf-8"))
    for key in ("loss_by_step", "train_loss_by_step", "loss_history"):
        rows = data.get(key)
        if isinstance(rows, list) and rows:
            return _rows_to_df(rows)
    log = data.get("log_history")
    if isinstance(log, list) and log:
        return _log_history_to_df(log)
    return None


def load_from_trainer_state() -> pd.DataFrame | None:
    if not TRAINER_STATE_JSON.exists():
        return None
    state = json.loads(TRAINER_STATE_JSON.read_text(encoding="utf-8"))
    log = state.get("log_history")
    if not isinstance(log, list):
        return None
    return _log_history_to_df(log, train_only=True)


def _log_history_to_df(log: list, train_only: bool = False) -> pd.DataFrame:
    rows: list[dict] = []
    for entry in log:
        if not isinstance(entry, dict):
            continue
        if train_only and "eval_loss" in entry and "loss" not in entry:
            continue
        loss = entry.get("loss")
        if loss is None:
            continue
        step = entry.get("step", entry.get("global_step", len(rows)))
        rows.append({"global_step": int(step), "loss": float(loss)})
    if not rows:
        raise RuntimeError("No train loss rows in log_history")
    return pd.DataFrame(rows).sort_values("global_step").reset_index(drop=True)


def _rows_to_df(rows: list) -> pd.DataFrame:
    if isinstance(rows[0], dict):
        step_key = "global_step" if "global_step" in rows[0] else "step"
        return pd.DataFrame(
            [{"global_step": int(r[step_key]), "loss": float(r["loss"])} for r in rows]
        ).sort_values("global_step")
    return pd.DataFrame(rows, columns=["global_step", "loss"]).sort_values("global_step")


def _plot_margins(w: int, h: int) -> tuple[int, int, int, int]:
    """Axis box for the legacy 1650x750 chart or proportional fallback."""
    if w >= 1500:
        return 167, 1540, 82, 635
    return int(w * 0.10), int(w * 0.93), int(h * 0.11), int(h * 0.85)


def digitize_legacy_png(step_max: int) -> pd.DataFrame:
    """Recover train-loss curve from legacy matplotlib PNG (train line only, no eval)."""
    from PIL import Image

    if not LEGACY_PNG.exists():
        raise FileNotFoundError(
            f"No loss_by_step.csv or JSON logs found, and missing {LEGACY_PNG}"
        )

    img = np.array(Image.open(LEGACY_PNG).convert("RGB"))
    h, w = img.shape[:2]
    r, g, b = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
    train_mask = (b > 155) & (r < 95) & (g > 95) & (b > r + 40) & (b > g)
    orange_mask = (r > 200) & (g > 90) & (g < 200) & (b < 130)

    x0, x1, y0, y1 = _plot_margins(w, h)
    # Stop before eval marker / legend on the right.
    for x in range(x1, x0, -1):
        if orange_mask[y0:y1, x].any():
            x1 = max(x0 + 50, x - 8)
    x1 = min(x1, w - 1)

    loss_hi, loss_lo = 7.5, 4.5
    loss_valid = (4.7, 7.35)  # train line only (excludes margin misreads at 7.5)

    samples: list[tuple[float, float]] = []
    for x in range(x0, x1 + 1):
        col = train_mask[:, x]
        if not col.any():
            continue
        ys = np.where(col)[0]
        y = int(np.median(ys))
        loss = loss_hi - (y - y0) / (y1 - y0) * (loss_hi - loss_lo)
        if not (loss_valid[0] <= loss <= loss_valid[1]):
            continue
        step = (x - x0) / (x1 - x0) * step_max
        samples.append((step, loss))

    if not samples:
        raise RuntimeError(f"Could not extract train line from {LEGACY_PNG}")

    rough = pd.DataFrame(samples, columns=["global_step", "loss"]).sort_values("global_step")
    steps = np.arange(0, step_max + 1)
    losses = np.interp(steps, rough["global_step"], rough["loss"])
    df = pd.DataFrame({"global_step": steps.astype(int), "loss": losses})

    stats = DATA_DIR / "training_stats.txt"
    if stats.exists():
        m = re.search(r"last_logged_train_loss\s*=\s*([\d.]+)", stats.read_text(encoding="utf-8"))
        if m:
            target = float(m.group(1))
            # Blend last ~1% of steps toward logged final loss if digitization drifts.
            tail_n = max(1, step_max // 100)
            tail_idx = df["global_step"] >= (step_max - tail_n)
            df.loc[tail_idx, "loss"] = np.linspace(
                float(df.loc[~tail_idx, "loss"].iloc[-1]),
                target,
                int(tail_idx.sum()),
            )

    return df


def load_step_data(force_digitize: bool = False) -> tuple[pd.DataFrame, str]:
    if not force_digitize:
        for loader, name in (
            (load_from_csv, "loss_by_step.csv"),
            (load_from_training_stats_json, "training_stats.json"),
            (load_from_trainer_state, "trainer_state.json"),
        ):
            df = loader()
            if df is not None:
                return df, name

    step_max = _read_global_steps_cap()
    return digitize_legacy_png(step_max), f"digitized:{LEGACY_PNG.name}"


def add_epoch_column(df: pd.DataFrame) -> pd.DataFrame:
    step_max = int(df["global_step"].max())
    n_epochs = 1
    if TRAINING_REPORT.exists():
        m = re.search(r"epochs?:\s*(\d+)", TRAINING_REPORT.read_text(encoding="utf-8"), re.I)
        # training_stats uses epochs in separate file
    stats = DATA_DIR / "training_stats.txt"
    if stats.exists():
        m = re.search(r"epochs\s*=\s*([\d.]+)", stats.read_text(encoding="utf-8"))
        if m:
            n_epochs = max(1, int(float(m.group(1))))
    steps_per_epoch = max(1, step_max // n_epochs)

    def step_to_epoch(step: int) -> int:
        return min(int(step) // steps_per_epoch, n_epochs - 1)

    out = df.copy()
    out["epoch"] = out["global_step"].map(step_to_epoch)
    return out


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
    import sys

    force_digitize = "--force-digitize" in sys.argv or "--from-png" in sys.argv

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df, source = load_step_data(force_digitize=force_digitize)
    df = add_epoch_column(df)
    epoch_df = epoch_means_from_steps(df)

    df[["global_step", "epoch", "loss"]].to_csv(
        OUT_DIR / "training_loss_by_step.csv", index=False
    )
    df[["global_step", "loss"]].to_csv(DATA_DIR / "loss_by_step.csv", index=False)
    epoch_df.to_csv(OUT_DIR / "training_loss_by_epoch.csv", index=False)

    plot_loss_by_step(df, OUT_DIR / "training_loss_by_step.png")
    plot_loss_by_step(df, OUT_DIR / "grafico_perda_ajuste_fino_orpheus_por_passo.png")
    plot_loss_by_epoch(epoch_df, OUT_DIR / "training_loss_by_epoch.png")
    plot_loss_by_epoch(epoch_df, OUT_DIR / "grafico_perda_ajuste_fino_orpheus_por_epoca.png")
    plot_combined(df, epoch_df, OUT_DIR / "training_loss_step_and_epoch.png")

    plot_loss_by_step(df, DATA_DIR / "loss_curve_by_step.png")
    plot_loss_by_epoch(epoch_df, DATA_DIR / "loss_curve_by_epoch.png")
    plot_loss_by_step(df, DATA_DIR / "loss_curve.png")

    print(f"Source: {source}")
    print(f"Parsed {len(df)} train loss points, epochs {df['epoch'].min()}-{df['epoch'].max()}")
    print(f"Mean loss: {df['loss'].mean():.4f}, last: {df['loss'].iloc[-1]:.4f}")
    print(f"Wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
