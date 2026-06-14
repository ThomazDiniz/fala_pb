# Conclusões preliminares — Original vs Ajustado

Base: CSV2 (melhor das 3 repetições). Pareado por índice de sentença.
Δ = média(ajustado) − média(original). **Δ > 0 ⇒ ajustado melhor**.

## fishspeech

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.854 | 0.890 | +0.036 | 0.318 | sem diferença sig. |
| mos_principal | 3.754 | 3.645 | -0.108 | 0.003 | degradou* |
| nisqa_overall | 3.754 | 3.645 | -0.108 | 0.003 | degradou* |
| dns_ovrl | 3.658 | 3.678 | +0.020 | 0.827 | sem diferença sig. |

## unsloth

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.880 | 0.553 | -0.327 | 0.000 | degradou* |
| mos_principal | 4.868 | 3.876 | -0.991 | 0.000 | degradou* |
| nisqa_overall | 4.868 | 3.876 | -0.991 | 0.000 | degradou* |
| dns_ovrl | 4.048 | 3.436 | -0.612 | 0.000 | degradou* |

## xtts

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.998 | 0.862 | -0.136 | 0.000 | degradou* |
| mos_principal | 3.216 | 3.535 | +0.319 | 0.000 | ajustado melhor* |
| nisqa_overall | 3.216 | 3.535 | +0.319 | 0.000 | ajustado melhor* |
| dns_ovrl | 3.618 | 3.595 | -0.023 | 0.647 | sem diferença sig. |

\* p < 0,05.

> Levenshtein menor no ajustado ⇒ perda de inteligibilidade; MOS menor ⇒ perda de qualidade. Δ≈0 e p≥0,05 ⇒ a adaptação de sotaque não degradou significativamente. Conclusões automáticas/preliminares; validação final = teste perceptivo humano.