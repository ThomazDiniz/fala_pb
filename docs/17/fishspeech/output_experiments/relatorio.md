# Relatório do experimento de fine-tuning — corpus Paraíba (pt-BR)

**Identificador:** `paraiba_20260510_031412`  
**Data de referência do relatório:** 16 de maio de 2026  
**Pipeline:** Fish Speech v1.5 (`fishaudio/fish-speech-1.5`) — adaptação LoRA text2semantic + codec VQGAN Firefly  

Este documento resume configuração, treino, métricas e saídas de áudio do experimento, para uso na dissertação. Os ficheiros correspondentes estão organizados nesta pasta (`output_experiments/`).

---

## 1. Objetivo

Ajustar o modelo **Fish Speech 1.5** (LLaMA semântico + VQGAN) a segmentos de fala em **português brasileiro** do corpus **Paraíba** (`filtered_char`), via **fine-tuning LoRA**, e avaliar qualitativamente a síntese com **cinco frases de teste** em pt-BR, comparando:

- modelo **pré-treinado** (baseline, sem LoRA fundido);
- modelo **fine-tuned** (checkpoint `step_000010488` após merge LoRA).

---

## 2. Modelo e adaptação

| Item | Valor |
|------|--------|
| Modelo base (Hub) | `fishaudio/fish-speech-1.5` |
| Código | Fish Speech tag **v1.5.0** (imagem Docker `fishspeech-paraiba:1.5.0`) |
| Tarefa | `text2semantic_finetune` (TextToSemantic) |
| Adaptação | **LoRA** (`r=8`, `lora_alpha=16`, `lora_dropout=0.01`) |
| Config Hydra LoRA | `r_8_alpha_16` |
| Codec áudio | VQGAN **Firefly** (`firefly_gan_vq`), checkpoint `firefly-gan-vq-fsq-8x1024-21hz-generator.pth` |
| Parâmetros totais | 644 092 416 |
| Parâmetros treináveis (LoRA) | 6 171 136 (~0,96% do total) |
| Checkpoint LoRA guardado | `step_000010488.ckpt` (~35,7 MiB) — apenas pesos adaptadores |
| Pesos LLaMA fundidos | `../final_merged_llama/` (gerado por `merge_lora.py` após o treino) |

O tamanho reduzido do `.ckpt` é esperado: guarda sobretudo tensores LoRA, não o modelo completo (~centenas de MiB).

---

## 3. Dataset

| Métrica | Valor |
|---------|--------|
| Origem | `filtered_char/metadata.csv` + `filtered_char/wavs/` |
| Speaker ID | `PB_PARAIBA` |
| Idioma | pt-BR |
| Linhas lidas no metadata | 41 953 |
| Segmentos aceites | **41 952** |
| Descartados | 1 (`invalid_segment_id`) |
| Duração média (ficheiro `duration.json`, amostra) | ~3,93 s (mediana ~3,3 s) |
| Horas estimadas de áudio (metadata) | ~44,8 h |
| Caracteres por linha (média / mediana) | 59,9 / 44 |
| Palavras por linha (média / mediana) | 11,7 / 9 |

**Nota operacional:** no ambiente Windows, os ficheiros `.wav` em `prep/data` apareceram com **0 bytes** (placeholders, p.ex. OneDrive). O treino utilizou os **tokens semânticos** já extraídos (`segment_*.npy`). Na inferência, o prompt de referência foi obtido a partir de `segment_1.npy` (decodificado para `reference_prompt.wav`), não de um WAV original em disco.

---

## 4. Hiperparâmetros de treino

| Hiperparâmetro | Valor |
|----------------|--------|
| `trainer.max_steps` | **10 488** |
| Épocas sintéticas (`NUM_TRAIN_EPOCHS`) | 1 |
| Steps por época sintética | 10 488 = ⌈41 952 / (4×1×1)⌉ |
| `data.batch_size` | 4 |
| `trainer.accumulate_grad_batches` | 1 |
| Efetivo amostras/step | 4 |
| `model.optimizer.lr` | **1×10⁻⁴** (AdamW, β=(0,9; 0,95), ε=1×10⁻⁵) |
| Warmup LR | 10 steps |
| `max_length` (tokens/texto) | 4096 |
| `data.num_workers` | 0 |
| `trainer.precision` | bf16-true |
| `trainer.devices` / GPUs | 1 |
| `trainer.log_every_n_steps` | 5 |
| `trainer.val_check_interval` | 10 488 (validação no fim da época) |
| `trainer.limit_val_batches` | 32 |
| `trainer.gradient_clip_val` | 1,0 (norm) |
| Checkpoint | `every_n_train_steps=10488`, `save_top_k=1` |
| Ficheiro guardado | `step_000010488.ckpt` |

Configuração completa: `config/hparams.yaml`.

---

## 5. Ambiente de execução

| Item | Valor |
|------|--------|
| SO (container) | Linux (WSL2 kernel 6.6.87) |
| Python | 3.11.10 |
| PyTorch | 2.5.1+cu124 (CUDA 12.4) |
| GPU | **NVIDIA GeForce RTX 4060 Ti** (1×) |
| CPU lógicos | 12 |
| RAM (container) | ~16 GiB |

Perfil detalhado: `config/machine_profile.json`.

---

## 6. Tempo de treino e métricas

| Métrica | Valor |
|---------|--------|
| Duração aproximada (wall clock, logs TensorBoard) | **~44,7 h** (~160 996 s) |
| Intervalo médio entre logs de treino | ~76,8 s (depende de `log_every_n_steps=5`) |
| Steps registados (treino) | 4 … 10 484 |
| **Loss treino** (step 4) | 9,50 |
| **Loss treino** (step 10 484) | 8,88 |
| **Loss treino média** (época sintética 1) | **9,026** |
| **eval_loss** (validação, step 10 487) | **8,963** |

Ficheiros: `metrics/train_loss_by_step.csv`, `metrics/eval_loss_synthetic_epoch.csv`, `metrics/timing_summary.json`.  
Gráficos: `plots/train_loss_by_step.png`, `plots/val_loss_by_step.png`, `plots/eval_loss_mean_by_epoch.png`, etc.

O treino Lightning **concluiu** e o checkpoint foi gravado; a fase pós-treino inicial falhou por scripts CRLF no Windows, mas foi **reexecutada com sucesso** (`SKIP_TRAIN=1`).

---

## 7. Protocolo de inferência (avaliação subjetiva)

| Item | Valor |
|------|--------|
| Frases de teste | 5 linhas em pt-BR (`config/inference_phrases_ptbr.txt`) |
| Dispositivo | CUDA |
| Prompt de referência | Transcrição de `segment_1` + tokens `segment_1.npy` |
| Baseline | Modelo base `fish-speech-1.5` (sem merge LoRA) → `audio/baseline_pretrained/baseline_phrase_0N.wav` |
| Fine-tuned | Merge LoRA de `step_000010488.ckpt` + `generate.py` + decode VQGAN → `audio/inference_finetuned/step_000010488_phrase_0N.wav` |

### Frases utilizadas

1. Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.  
2. Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.  
3. O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.  
4. Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.  
5. A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.

**Importante:** os ficheiros em `output/synthesized_speech_phrase_*.wav` (script `run_inference.bat` / `inference_demo.sh`) usam **apenas o modelo base**, não este checkpoint.

---

## 8. Estrutura desta pasta

```
output_experiments/
├── relatorio.md                          ← este ficheiro
├── checkpoint/
│   └── step_000010488.ckpt               ← adaptador LoRA final
├── config/
│   ├── hparams.yaml                      ← hiperparâmetros Lightning/Hydra
│   ├── dataset_stats.json
│   ├── dataset_text_stats.json
│   ├── machine_profile.json
│   ├── inference_phrases_ptbr.txt
│   ├── reference_prompt_transcript.txt
│   └── listening_comparison_manifest.json
├── metrics/                              ← CSVs e JSON de perdas/tempos
├── plots/                                ← gráficos PNG (loss, tempo)
└── audio/
    ├── reference/reference_prompt.wav
    ├── baseline_pretrained/baseline_phrase_01…05.wav
    └── inference_finetuned/step_000010488_phrase_01…05.wav
```

---

## 9. Síntese para a dissertação (texto corrido)

Foi realizado fine-tuning **LoRA** (r=8, α=16) sobre o Fish Speech 1.5, com **10 488** passos de otimização (uma época sintética sobre 41 952 segmentos, batch 4, LR 10⁻⁴, precisão bf16), em **uma GPU RTX 4060 Ti**, com duração de treino da ordem de **45 horas**. O adaptador final ocupa cerca de **36 MiB**; a loss de treino média na época foi **9,03** e o **eval_loss** **8,96**. A avaliação perceptiva usou cinco frases em português brasileiro, com o mesmo prompt de voz de referência (segmento 1 do corpus), comparando sínteses do modelo pré-treinado e do modelo com LoRA fundido no checkpoint `step_000010488`. Limitações: WAVs do corpus não estavam materializados no disco Windows durante o pós-processamento; tokens `.npy` e reconstrução VQGAN do prompt foram usados como alternativa.

---

## 10. Referências no repositório

- Diretivas do experimento: `EXPERIMENTO_DIRETIVAS.md` (raiz do projeto)
- Log completo do pipeline: `../train.log`
- Experimentação original: `../` (pasta `experiments/paraiba_20260510_031412/`)
