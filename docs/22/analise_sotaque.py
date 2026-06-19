#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise robusta da avaliacao manual (preferencia par-a-par) de sotaque
paraibano e inteligibilidade em falas sintetizadas.

Tres blocos:
  BLOCO 1 - Original vs Adaptado (XTTS, FishSpeech, Unsloth/Orpheus)
            -> responde Q1 (sotaque adicionado?) e Q2 (ajuste melhora/piora?)
  BLOCO 2 - Ranqueamento head-to-head entre os 3 modelos adaptados
            -> responde Q3 (qual modelo campeao em sotaque e inteligibilidade?)

Saidas: impressao no stdout + arquivo resultados.json
"""
import csv, json
from collections import Counter, defaultdict
from scipy.stats import binomtest

CSV = "Avaliação de Sotaque Paraibano em Falas Sintetizadas xtts (respostas) - Respostas ao formulário 1.csv"

with open(CSV, encoding="utf-8") as f:
    rows = list(csv.reader(f))
header, data = rows[0], rows[1:]
N = len(data)

A, B = "Áudio A", "Áudio B"
AMBOS_SOT = "Ambos aparentam ter sotaque paraibano"
AMBOS_INT = "Ambos soam igualmente bem"
NAODIST = "Não consigo distinguir"

FAM_COL = 2
def is_paraibano(v):
    return v.strip() == "Sou da paraíba"

# ----------------------------------------------------------------------------
# BLOCO 1: Original vs Adaptado
# pares = (col_sotaque, col_intelig, letra_do_modelo_ADAPTADO)
# ----------------------------------------------------------------------------
BLOCO1 = {
    "XTTS": [(3, 4, "B"), (5, 6, "A"), (7, 8, "B")],
    "FishSpeech": [(9, 10, "A"), (11, 12, "B"), (13, 14, "B")],
    "Unsloth/Orpheus": [(15, 16, "B"), (17, 18, "A"), (19, 20, "B")],
}

def letra(opt):
    if opt == A: return "A"
    if opt == B: return "B"
    return None

def analisa_bloco1(subset):
    out = {}
    for modelo, pares in BLOCO1.items():
        sot = Counter(); intg = Counter()
        por_amostra = []
        for (cs, ci, adapt) in pares:
            orig = "A" if adapt == "B" else "B"
            s = Counter(); itc = Counter()
            for row in subset:
                l = letra(row[cs])
                if l == adapt: s["adaptado"] += 1
                elif l == orig: s["original"] += 1
                elif row[cs] == AMBOS_SOT: s["ambos"] += 1
                else: s["naodist"] += 1
                l2 = letra(row[ci])
                if l2 == adapt: itc["adaptado"] += 1
                elif l2 == orig: itc["original"] += 1
                elif row[ci] == AMBOS_INT: itc["ambos"] += 1
                else: itc["naodist"] += 1
            sot.update(s); intg.update(itc)
            por_amostra.append({"cols": (cs, ci), "adaptado": adapt,
                                "sotaque": dict(s), "intelig": dict(itc)})
        n = len(subset) * len(pares)
        pos_sot = sot["adaptado"] + sot["ambos"]
        sot_dec = sot["adaptado"] + sot["original"]
        bt_sot = binomtest(sot["adaptado"], sot_dec, 0.5, "greater").pvalue if sot_dec else None
        pos_int = intg["adaptado"] + intg["ambos"]
        int_dec = intg["adaptado"] + intg["original"]
        bt_int = binomtest(intg["adaptado"], int_dec, 0.5, "greater").pvalue if int_dec else None
        out[modelo] = {
            "n_respostas": n, "n_respondentes": len(subset), "n_amostras": len(pares),
            "sotaque": dict(sot), "intelig": dict(intg),
            "pct_sotaque_adicionado": round(100*pos_sot/n, 1),
            "pct_sot_adaptado": round(100*sot["adaptado"]/n, 1),
            "pct_sot_ambos": round(100*sot["ambos"]/n, 1),
            "pct_sot_original": round(100*sot["original"]/n, 1),
            "pct_sot_naodist": round(100*sot["naodist"]/n, 1),
            "binom_p_sotaque": bt_sot,
            "pct_intelig_naopior": round(100*pos_int/n, 1),
            "pct_int_adaptado": round(100*intg["adaptado"]/n, 1),
            "pct_int_ambos": round(100*intg["ambos"]/n, 1),
            "pct_int_original": round(100*intg["original"]/n, 1),
            "pct_int_naodist": round(100*intg["naodist"]/n, 1),
            "binom_p_intelig": bt_int,
            "por_amostra": por_amostra,
        }
    return out

# ----------------------------------------------------------------------------
# BLOCO 2: head-to-head entre modelos adaptados
# ----------------------------------------------------------------------------
BLOCO2 = {
    "XTTS_vs_FishSpeech": {"A": "XTTS", "B": "FishSpeech",
        "pares": [(21, 22), (23, 24), (25, 26)]},
    "FishSpeech_vs_Unsloth": {"A": "FishSpeech", "B": "Unsloth/Orpheus",
        "pares": [(27, 28), (29, 30), (31, 32)]},
    "XTTS_vs_Unsloth": {"A": "XTTS", "B": "Unsloth/Orpheus",
        "pares": [(33, 34), (35, 36), (37, 38)]},
}

def analisa_bloco2(subset):
    confrontos = {}
    wins = defaultdict(lambda: {"sot_win": 0, "sot_loss": 0, "sot_tie": 0,
                                "int_win": 0, "int_loss": 0, "int_tie": 0})
    for nome, cfg in BLOCO2.items():
        mA, mB = cfg["A"], cfg["B"]
        sot = Counter(); intg = Counter()
        for (cs, ci) in cfg["pares"]:
            for row in subset:
                if row[cs] == A: sot["A"] += 1
                elif row[cs] == B: sot["B"] += 1
                elif row[cs] == AMBOS_SOT: sot["ambos"] += 1
                else: sot["naodist"] += 1
                if row[ci] == A: intg["A"] += 1
                elif row[ci] == B: intg["B"] += 1
                elif row[ci] == AMBOS_INT: intg["ambos"] += 1
                else: intg["naodist"] += 1
        n = len(subset) * len(cfg["pares"])
        wins[mA]["sot_win"] += sot["A"]; wins[mA]["sot_loss"] += sot["B"]
        wins[mB]["sot_win"] += sot["B"]; wins[mB]["sot_loss"] += sot["A"]
        wins[mA]["sot_tie"] += sot["ambos"]; wins[mB]["sot_tie"] += sot["ambos"]
        wins[mA]["int_win"] += intg["A"]; wins[mA]["int_loss"] += intg["B"]
        wins[mB]["int_win"] += intg["B"]; wins[mB]["int_loss"] += intg["A"]
        wins[mA]["int_tie"] += intg["ambos"]; wins[mB]["int_tie"] += intg["ambos"]
        d_sot = sot["A"] + sot["B"]
        d_int = intg["A"] + intg["B"]
        confrontos[nome] = {
            "modeloA": mA, "modeloB": mB, "n": n,
            "sotaque": dict(sot), "intelig": dict(intg),
            "sot_pct_A": round(100*sot["A"]/n,1), "sot_pct_B": round(100*sot["B"]/n,1),
            "sot_pct_ambos": round(100*sot["ambos"]/n,1),
            "int_pct_A": round(100*intg["A"]/n,1), "int_pct_B": round(100*intg["B"]/n,1),
            "int_pct_ambos": round(100*intg["ambos"]/n,1),
            "binom_p_sot_A_maior": binomtest(sot["A"], d_sot, 0.5, "greater").pvalue if d_sot else None,
            "binom_p_int_A_maior": binomtest(intg["A"], d_int, 0.5, "greater").pvalue if d_int else None,
        }
    ranking = {}
    for m, w in wins.items():
        sot_dec = w["sot_win"] + w["sot_loss"]
        int_dec = w["int_win"] + w["int_loss"]
        ranking[m] = {
            **w,
            "sot_winrate": round(100*w["sot_win"]/sot_dec,1) if sot_dec else None,
            "int_winrate": round(100*w["int_win"]/int_dec,1) if int_dec else None,
        }
    return confrontos, ranking

def run(subset, label):
    print("\n" + "="*78)
    print(f"SUBGRUPO: {label}  (n={len(subset)} respondentes)")
    print("="*78)
    b1 = analisa_bloco1(subset)
    for modelo, r in b1.items():
        print(f"\n--- {modelo}  (3 amostras x {r['n_respondentes']} = {r['n_respostas']} respostas) ---")
        print(f"  SOTAQUE: adaptado={r['pct_sot_adaptado']}%  ambos={r['pct_sot_ambos']}%  "
              f"original={r['pct_sot_original']}%  naodist={r['pct_sot_naodist']}%")
        print(f"     -> Q1 sotaque ADICIONADO (adaptado+ambos) = {r['pct_sotaque_adicionado']}%  "
              f"(binom adaptado>original p={r['binom_p_sotaque']:.2e})")
        print(f"  INTELIG: adaptado={r['pct_int_adaptado']}%  ambos={r['pct_int_ambos']}%  "
              f"original={r['pct_int_original']}%  naodist={r['pct_int_naodist']}%")
        print(f"     -> Q2 ajuste NAO PIORA (adaptado+ambos) = {r['pct_intelig_naopior']}%  "
              f"(binom adaptado>original p={r['binom_p_intelig']:.2e})")
    c2, rank = analisa_bloco2(subset)
    print(f"\n--- BLOCO 2: confrontos diretos ---")
    for nome, c in c2.items():
        print(f"  {nome}: SOT {c['modeloA']}={c['sot_pct_A']}% {c['modeloB']}={c['sot_pct_B']}% ambos={c['sot_pct_ambos']}% | "
              f"INT {c['modeloA']}={c['int_pct_A']}% {c['modeloB']}={c['int_pct_B']}% ambos={c['int_pct_ambos']}%")
    print(f"\n--- RANKING (taxa de vitoria, empates excluidos) ---")
    for m, w in sorted(rank.items(), key=lambda x: -(x[1]['sot_winrate'] or 0)):
        print(f"  {m:18s} SOT winrate={w['sot_winrate']}% (W{w['sot_win']}/L{w['sot_loss']}/E{w['sot_tie']})  "
              f"INT winrate={w['int_winrate']}% (W{w['int_win']}/L{w['int_loss']}/E{w['int_tie']})")
    return {"bloco1": b1, "bloco2_confrontos": c2, "bloco2_ranking": rank,
            "n_respondentes": len(subset)}

results = {}
results["TODOS"] = run(data, "TODOS os respondentes")
par = [r for r in data if is_paraibano(r[FAM_COL])]
results["PARAIBANOS"] = run(par, "Apenas 'Sou da paraiba'")
fam = [r for r in data if "pouca ou nenhuma" not in r[FAM_COL].lower()]
results["FAMILIARIZADOS"] = run(fam, "Paraibanos + familiarizados (exclui 'pouca/nenhuma')")

with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\n\n[OK] resultados.json salvo.")
print("Distribuicao familiaridade:")
for k, v in Counter(r[FAM_COL] for r in data).items():
    print(f"  {v:3d}  {k}")
