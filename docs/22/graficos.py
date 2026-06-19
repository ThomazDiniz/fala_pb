#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(BASE, "figs")
os.makedirs(FIGS, exist_ok=True)
R = json.load(open(os.path.join(BASE, "resultados.json"), encoding="utf-8"))
T = R["TODOS"]
MODELOS = ["XTTS", "FishSpeech", "Unsloth/Orpheus"]
DISP = {"XTTS": "XTTS", "FishSpeech": "FishSpeech", "Unsloth/Orpheus": "Orpheus"}

C_ADAPT = "#2a9d8f"; C_AMBOS = "#8ecae6"; C_ORIG = "#e76f51"; C_ND = "#bcbcbc"
OUT_DARK = [pe.withStroke(linewidth=2.6, foreground="black")]
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

def stacked(ax, dom, title):
    adapt = [T["bloco1"][m]["pct_%s_adaptado" % dom] for m in MODELOS]
    ambos = [T["bloco1"][m]["pct_%s_ambos" % dom] for m in MODELOS]
    orig  = [T["bloco1"][m]["pct_%s_original" % dom] for m in MODELOS]
    nd    = [T["bloco1"][m]["pct_%s_naodist" % dom] for m in MODELOS]
    y = np.arange(len(MODELOS))
    nd_lab = "Entrevistado nao conseguiu distinguir".replace("nao", "não")
    if dom == "sot":
        labels = ("Adaptado tem mais sotaque", "Ambos têm sotaque",
                  "Original tem mais sotaque", nd_lab)
    else:
        labels = ("Adaptado é melhor", "Ambos igualmente bons",
                  "Original é melhor", nd_lab)
    left = np.zeros(len(MODELOS))
    for vals, col, lab in [(adapt, C_ADAPT, labels[0]), (ambos, C_AMBOS, labels[1]),
                           (orig, C_ORIG, labels[2]), (nd, C_ND, labels[3])]:
        ax.barh(y, vals, left=left, color=col, label=lab, edgecolor="white")
        for yi, (v, l0) in enumerate(zip(vals, left)):
            if v >= 4:
                ax.text(l0 + v/2, yi, "%.0f%%" % v, va="center", ha="center",
                        color="white", fontsize=9, fontweight="bold", path_effects=OUT_DARK)
        left += np.array(vals)
    ax.set_yticks(y); ax.set_yticklabels([DISP[m] for m in MODELOS])
    ax.set_xlim(0, 100); ax.set_xlabel("% das respostas")
    ax.invert_yaxis(); ax.set_title(title, fontweight="bold")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=2, frameon=False, fontsize=9)

fig, ax = plt.subplots(figsize=(9, 4.2))
stacked(ax, "sot", "Percepção de sotaque paraibano: Original × Adaptado")
plt.tight_layout(); plt.savefig(os.path.join(FIGS, "q1_sotaque.png"), dpi=150, bbox_inches="tight"); plt.close()

fig, ax = plt.subplots(figsize=(9, 4.2))
stacked(ax, "int", "Clareza e Naturalidade: Original × Adaptado")
plt.tight_layout(); plt.savefig(os.path.join(FIGS, "q2_inteligibilidade.png"), dpi=150, bbox_inches="tight"); plt.close()

fig, ax = plt.subplots(figsize=(8, 4.5))
sot = [T["bloco2_ranking"][m]["sot_winrate"] for m in MODELOS]
itg = [T["bloco2_ranking"][m]["int_winrate"] for m in MODELOS]
x = np.arange(len(MODELOS)); w = 0.36
b1 = ax.bar(x - w/2, sot, w, label="Sotaque", color="#264653")
b2 = ax.bar(x + w/2, itg, w, label="Clareza e Naturalidade", color="#e9c46a")
ax.axhline(50, ls="--", color="gray", lw=1)
ax.text(2.45, 51.5, "50% (empate)", color="gray", fontsize=8, ha="right")
for b in list(b1) + list(b2):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5,
            "%.0f%%" % b.get_height(), ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels([DISP[m] for m in MODELOS])
ax.set_ylim(0, 100); ax.set_ylabel("Taxa de vitória (empates excluídos)")
ax.set_title("Ranqueamento entre modelos ajustados (confrontos diretos)", fontweight="bold")
ax.legend(frameon=False)
plt.tight_layout(); plt.savefig(os.path.join(FIGS, "q3_ranking.png"), dpi=150, bbox_inches="tight"); plt.close()

nomes = list(T["bloco2_confrontos"].keys())
fig, axes = plt.subplots(len(nomes), 2, figsize=(13, 7.2))
col_titles = ["Sotaque", "Clareza e Naturalidade"]
for ri, n in enumerate(nomes):
    c = T["bloco2_confrontos"][n]
    mA, mB = DISP[c["modeloA"]], DISP[c["modeloB"]]
    for ci, dom in enumerate(["sot", "int"]):
        ax = axes[ri][ci]
        vals = [c["%s_pct_A" % dom], c["%s_pct_ambos" % dom], c["%s_pct_B" % dom]]
        labs = [mA, "Empate / ambos", mB]
        cols = [C_ADAPT, C_AMBOS, C_ORIG]
        winA = vals[0] >= vals[2]
        weights = ["bold" if winA else "normal", "normal", "bold" if not winA else "normal"]
        yy = np.arange(3)
        ax.barh(yy, vals, color=cols, edgecolor="white")
        for yi, v in enumerate(vals):
            ax.text(v + 1.5, yi, "%.0f%%" % v, va="center", ha="left",
                    fontsize=9, fontweight="bold")
        ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=9)
        for tick, wt in zip(ax.get_yticklabels(), weights):
            tick.set_fontweight(wt)
        ax.invert_yaxis()
        ax.set_xlim(0, 100); ax.set_xticks(range(0, 101, 20))
        ax.grid(axis="x", ls=":", color="#ddd"); ax.set_axisbelow(True)
        if ri == 0:
            ax.set_title(col_titles[ci], fontweight="bold")
        if ri == len(nomes) - 1:
            ax.set_xlabel("% das respostas")
    axes[ri][0].annotate("%s × %s" % (mA, mB), xy=(-0.30, 0.5),
                         xycoords="axes fraction", rotation=90, va="center", ha="center",
                         fontsize=10, fontweight="bold", annotation_clip=False)
fig.suptitle("Confrontos diretos par-a-par", fontweight="bold", y=0.99)
plt.tight_layout(rect=[0.04, 0, 1, 0.97])
plt.savefig(os.path.join(FIGS, "q3_confrontos.png"), dpi=150, bbox_inches="tight"); plt.close()
print("OK figs:", os.listdir(FIGS))
