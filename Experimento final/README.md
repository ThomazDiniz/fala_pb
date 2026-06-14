# Experimento Final — análise objetiva (Levenshtein + preditores de MOS)

**Rode um único script:** `experimento_final.py`
(baseado no seu `avaliador/avaliador.py`, mesmas libs e métricas).

Compara **original** (checkpoint antes do fine-tune) vs **ajustado** (com sotaque
paraibano) em 3 stacks de TTS, sobre os 1800 áudios em:

    docs/Inferencias finais/Audios/<modelo>/outputs_final_experiment/<condicao>/<vN>/NNN.wav
      <modelo>=fishspeech|unsloth|xtts ; <condicao>=original|ajustado ; <vN>=v1|v2|v3 ; NNN=001..100

O script faz tudo de uma vez:
1. STT com Whisper (small, pt) + distância/similaridade de **Levenshtein** vs `sentenças.txt`
2. preditores de **MOS**: **NISQA + DNSMOS** (torchmetrics)  — MOSA-Net é opcional (ver `mosanet/`)
3. **CSV1** `resultados/csv1_todas_metricas.csv` — todas as métricas, 1800 linhas
4. **CSV2** `resultados/csv2_melhor_de_3.csv` — melhor das 3 repetições (score composto Lev+MOS)
5. **gráficos** em `resultados/plots/` + `resultados/conclusoes_preliminares.md` (Δ ajustado−original + Wilcoxon)

Cada CSV também é salvo numa cópia `*_ptbr-excel.csv` (sep `;`, vírgula decimal) que abre direto no Excel pt-BR.

## Como rodar (sua máquina, com GPU)

    cd "Experimento final"
    pip install -r requirements.txt
    python experimento_final.py --limit 30    # teste rápido primeiro
    python experimento_final.py               # lote completo (1800 áudios), resumível

Outras opções: `--overwrite` (recalcula tudo), `--only-agg` (só refaz CSV2/gráficos do CSV1),
`--device cuda|cpu`, `--workers N` (áudios em paralelo; **padrão 5**).

**Paralelização:** `--workers` processa N áudios ao mesmo tempo, cada um num processo com
sua cópia dos modelos. Cada processo usa ~1–2 GB de RAM (Whisper). O script reduz N
automaticamente se você tiver menos núcleos, e avisa se a RAM pode apertar. Se travar,
rode com `--workers 2` ou `3`. Em GPU, normalmente `--workers 1` já é o mais rápido.

## Ajustes rápidos (topo do script)
- `WHISPER_MODEL` (default `small`)
- `PESO_LEV` / `PESO_MOS` (default 0.5/0.5) — peso da inteligibilidade vs qualidade no CSV2
- `MOS_PREFERENCIA` — qual MOS vira o "principal" (mosanet → nisqa → dnsmos)
- `USAR_MOSANET = True` para ativar o MOSA-Net (requer setup em `mosanet/`)

Detalhes da metodologia e fórmulas: `diretivas.md`.
