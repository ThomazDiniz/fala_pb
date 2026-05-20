# Relatório do experimento — pb_001

*Gerado em:* 2026-05-20T13:58:23.836559+00:00

## 1. Objetivo

Fine-tune do **Qwen3-TTS-12Hz-1.7B-Base** para sotaque/voz **pb_sotaque** (dataset `filtered_char`, ref `segment_0.wav`).

## 2. Dataset e pré-processamento

- Amostras no treino (com codes): **41952**
- Ref de áudio: `/workspace/filtered_char/wavs/segment_0.wav`
- Duração total do áudio (stats): **161275 s** (média **3.93 s**/amostra)

## 3. Hiperparâmetros de treino

| Parâmetro | Valor |
|-----------|-------|
| Modelo inicial | Qwen/Qwen3-TTS-12Hz-1.7B-Base |
| Speaker | pb_sotaque |
| Épocas configuradas | 1 |
| Batch size (por GPU) | 2 |
| Gradient accumulation | 4 |
| Batch efetivo | 8 |
| Learning rate | 2e-06 |
| Precision | bf16 |
| Attention | sdpa |
| DataLoader workers | 2 |
| Log a cada N steps | 10 |
| Checkpoint a cada N steps | 5000 |
| Checkpoints mantidos (top-k) | 6 |
| Steps por época | 20976 |
| Amostras | 41952 |

## 4. Tempo de execução

### 4.1 Até o último log (run em andamento ou completo)

- **Início (1º log):** 2026-05-17T03:12:51Z
- **Fim (último log na janela):** 2026-05-20T12:32:18Z
- **Último step na janela:** **17151** / **20976**
- **Tempo total (parede):** **3 dia(s), 9 h, 19 min, 27 s** (292767 s)
- **Tempo médio por step:** ~**17.1 s** (mediana ~16.4 s)
- **Estimativa 1 época completa:** ~**4 dia(s), 3 h, 28 min, 1 s**

- **Progresso atual:** **17151** / **20976** (81.8% da época)
### 4.2 Até o checkpoint step 15000

- **Início (1º log):** 2026-05-17T03:12:51Z
- **Fim (último log na janela):** 2026-05-20T01:44:54Z
- **Último step na janela:** **14991** / **20976**
- **Tempo total (parede):** **2 dia(s), 22 h, 32 min, 3 s** (253923 s)
- **Tempo médio por step:** ~**16.9 s** (mediana ~16.4 s)
- **Estimativa 1 época completa:** ~**4 dia(s), 2 h, 42 min, 3 s**

*Tempos derivados de timestamps entre linhas TRAIN (log_every); cada ponto cobre N steps do DataLoader.*

## 5. Checkpoints gravados

| Step | Timestamp (UTC) | Speaker |
|------|-----------------|---------|
| 5000 | 2026-05-18T00:48:55Z | pb_sotaque |
| 10000 | 2026-05-19T02:07:17Z | pb_sotaque |
| 15000 | 2026-05-20T01:50:13Z | pb_sotaque |

## 6. Loss (resumo)

- Primeira loss logada: **12.2913**
- Última loss logada: **None**
- Pontos com **loss=nan** no log: **2**
- Gráficos: `artifacts/train_loss.png`, `artifacts/train_loss_smoothed.png`
- CSV: `artifacts/train_metrics.csv`

## 7. Inferência (outputs)

- Speaker: **pb_sotaque**
- Idioma: **Portuguese**
- Arquivos: `outputs/step_<N>_frase<M>.wav` (ver `outputs/manifest.csv`)
  - step **5000**: step_5000_frase1.wav, step_5000_frase2.wav, step_5000_frase3.wav, step_5000_frase4.wav, step_5000_frase5.wav
  - step **10000**: step_10000_frase1.wav, step_10000_frase2.wav, step_10000_frase3.wav, step_10000_frase4.wav, step_10000_frase5.wav
  - step **15000**: step_15000_frase1.wav, step_15000_frase2.wav, step_15000_frase3.wav, step_15000_frase4.wav, step_15000_frase5.wav

## 8. Questões / limitações para discussão no relatório

- Treino **recomeça do modelo base** em `RESUME_EXPERIMENT=1` (não restaura pesos no meio da época).
- Inferência usa `generate_custom_voice(speaker=pb_sotaque)` (slot 3000); treino injeta embedding dinâmico de `ref_audio` — caminhos diferentes.
- Sotaque pode ser sutil vs. baseline PT do Qwen; comparar `outputs/` com áudio base.
- Apareceram **NaN** na loss após ~step 17150 — investigar estabilidade / LR / mixed precision.
