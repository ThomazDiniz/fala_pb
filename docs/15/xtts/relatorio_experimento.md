# Relatório — fine-tune XTTS GPT

- **experiment_dir:** `E:\git\coqui-ai-TTS\data\xtts-experiments\ptbr-20260425-224952`
- **artifacts:** `E:\git\coqui-ai-TTS\data\xtts-experiments\ptbr-20260425-224952\artifacts`
- **UTC:** 2026-04-26T06:18:08.259776+00:00

## Tempos por etapa

### Preparação de dados (prep)

| Métrica | Valor |
| --- | --- |
| Modo | `existing_in_root` |
| Tempo interno dataset (prep/split/whisper) | 0.0 s |
| **Tempo de parede total etapa PREP** | **8.9 s** |

### Treino

| Métrica | Valor |
| --- | --- |
| Treino `train_gpt` (GPU/step) | 266 min 31.0 s (15991 s total) |
| Pós-processamento (logs, gráficos, JSON) | 0.5 s |
| **Total etapa treino (parede)** | **266 min 42.8 s (16003 s total)** |
| Épocas pedidas | 3 |

## Gráficos de perda (gerados em `artifacts/`)

- `training_loss_demo_callback.png` — perda por **global step** e/ou **época** (ver legenda no PNG).
- `training_loss_tensorboard.png` — perda por **global step** e/ou **época** (ver legenda no PNG).

- `training_loss_step_and_epoch.png` — painel superior: loss vs step; inferior: média por época.
- `training_loss_by_epoch.png` — só média por época.
- `training_loss_from_trainer_log.png` — loss vs step (parser do `trainer_0_log.txt`).
- `training_step_time_by_global_step.png` — tempo por step (métrica `step_time` do log) vs global step.
- `training_time_by_step.csv` — colunas: global_step, epoch, phase, step_time_s, loss, log_timestamp.
- `training_time_by_epoch.json` — tempo de parede aproximado por época (extensão dos carimbos TIME) e soma de `step_time` por época.
- `training_statistics.json` — min/máx/última loss (train/eval) e contagens de pontos.
- `machine_report_thesis.md` — texto sobre CPU, RAM, GPU e software para relatório/dissertação.

## Áudio (referência vs inferência pós fine-tune)

Pasta `artifacts/audio_compare/`: **5** pares `ref_XX.wav` + `infer_finetuned_XX.wav` (ver `manifest.json`).
- `infer_finetuned_01.wav`
- `infer_finetuned_02.wav`
- `infer_finetuned_03.wav`
- `infer_finetuned_04.wav`
- `infer_finetuned_05.wav`
- `ref_01.wav`
- `ref_02.wav`
- `ref_03.wav`
- `ref_04.wav`
- `ref_05.wav`

## Resumo do log do trainer

- Linhas de época capturadas no log: **3**
- Amostras de `step_time` no log: **2129**
- Tempo médio por step (log): **0.1288 s**

---
*Gerado automaticamente por `scripts/xtts_finetune_paraiba_experiment.py`.*
