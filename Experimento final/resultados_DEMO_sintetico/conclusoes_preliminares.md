# Conclusões preliminares — Original vs Ajustado

Base: CSV2 (melhor das 3 repetições por sentença, score composto Lev+MOS).
Pareamento por índice de sentença entre `original` e `ajustado`.
Δ = média(ajustado) − média(original). **Δ > 0 ⇒ o ajustado é melhor**.

## fishspeech

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.956 | 0.916 | -0.040 | 0.000 | degradou* |
| mos_principal | 4.001 | 3.944 | -0.057 | 0.063 | sem diferença sig. |
| nisqa_overall | 3.992 | 3.919 | -0.073 | 0.234 | sem diferença sig. |
| dns_ovrl | 3.480 | 3.557 | +0.077 | 0.207 | sem diferença sig. |
| squim_mos | 3.999 | 3.968 | -0.032 | 0.703 | sem diferença sig. |

## unsloth

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.903 | 0.882 | -0.021 | 0.006 | degradou* |
| mos_principal | 3.732 | 3.763 | +0.031 | 0.337 | sem diferença sig. |
| nisqa_overall | 3.713 | 3.782 | +0.069 | 0.058 | sem diferença sig. |
| dns_ovrl | 3.527 | 3.421 | -0.106 | 0.045 | degradou* |
| squim_mos | 3.718 | 3.733 | +0.015 | 0.611 | sem diferença sig. |

## xtts

| métrica | original | ajustado | Δ | p (Wilcoxon) | leitura |
|---|---|---|---|---|---|
| lev_sim | 0.959 | 0.963 | +0.005 | 0.690 | sem diferença sig. |
| mos_principal | 4.236 | 4.110 | -0.127 | 0.000 | degradou* |
| nisqa_overall | 4.177 | 4.113 | -0.064 | 0.089 | sem diferença sig. |
| dns_ovrl | 3.495 | 3.473 | -0.021 | 0.736 | sem diferença sig. |
| squim_mos | 4.245 | 4.111 | -0.134 | 0.009 | degradou* |

\* diferença estatisticamente significativa (p < 0,05).

> Interpretação: para a pergunta *“o fine-tuning degrada o modelo?”*, uma similaridade Levenshtein **mais baixa** no ajustado indicaria perda de inteligibilidade; um MOS **mais baixo**, perda de qualidade perceptual. Valores de Δ próximos de zero e p ≥ 0,05 sugerem que a adaptação de sotaque **não degradou** significativamente o modelo. Estas são conclusões automáticas e preliminares — a validação final é a avaliação perceptiva humana.