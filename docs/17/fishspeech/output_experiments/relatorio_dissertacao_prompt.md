# Fine-tuning Fish Speech 1.5 — corpus Paraíba (pt-BR)

> **Uso:** copie este ficheiro inteiro para outro prompt e peça redação de secções da dissertação.  
> **Escopo:** apenas o experimento Fish Speech (`paraiba_20260510_031412`).  
> **Data de referência:** 16/05/2026  
> **Pasta de artefatos:** `docs/17/fishspeech/output_experiments/`

---

## Identificação do experimento

| Campo | Valor |
|-------|--------|
| ID | `paraiba_20260510_031412` |
| Modelo base | `fishaudio/fish-speech-1.5` (Fish Speech **1.5**) |
| Código | tag **v1.5.0** (imagem Docker `fishspeech-paraiba:1.5.0`) |
| Tarefa | `text2semantic_finetune` (módulo TextToSemantic: LLaMA semântico + codec VQGAN) |
| Adaptação | **LoRA** (`r=8`, `lora_alpha=16`, `lora_dropout=0.01`) |
| Config Hydra LoRA | `r_8_alpha_16` |
| Codec áudio | VQGAN **Firefly** (`firefly_gan_vq`), `firefly-gan-vq-fsq-8x1024-21hz-generator.pth` |
| Checkpoint LoRA final | `step_000010488.ckpt` (~35,7 MiB) |
| Pesos fundidos pós-treino | `final_merged_llama/` (`merge_lora.py`) |

---

## Objetivo

Ajustar o **Fish Speech 1.5** a segmentos de fala em **português brasileiro** do corpus **Paraíba** (`filtered_char`), via **fine-tuning LoRA** no módulo text2semantic, e avaliar a síntese com **cinco frases de teste** em pt-BR, comparando apenas:

- modelo **pré-treinado** (baseline, sem LoRA fundido);
- modelo **fine-tuned** (checkpoint `step_000010488` após merge LoRA).

---

## Modelo e parâmetros treináveis

| Item | Valor |
|------|--------|
| Parâmetros totais | 644 092 416 |
| Parâmetros treináveis (LoRA) | 6 171 136 |
| Percentagem treinável | **~0,96%** |
| Tamanho do checkpoint LoRA | ~35,7 MiB (apenas adaptadores; não é o modelo completo) |

O `.ckpt` guarda sobretudo tensores LoRA, não o backbone completo (~centenas de MiB).

---

## Dataset

| Métrica | Valor |
|---------|--------|
| Origem | `filtered_char/metadata.csv` + `filtered_char/wavs/` |
| Speaker ID | `PB_PARAIBA` |
| Idioma | pt-BR |
| Linhas lidas no metadata | 41 953 |
| Segmentos aceites | **41 952** |
| Descartados | 1 (`invalid_segment_id`) |
| Duração média dos segmentos | **3,93 s** |
| Duração mediana | **3,3 s** |
| Horas estimadas de áudio | **~44,8 h** |
| Caracteres por linha (média / mediana) | **59,9** / **44** |
| Palavras por linha (média / mediana) | **11,7** / **9** |
| Linhas com flag heurística “pt” | **63,13%** |

**Definição de época sintética usada no treino:**

```
passos_por_epoca = ceil(41952 / (batch_size × grad_accum × num_gpus))
                 = ceil(41952 / 4) = 10 488
```

**Nota operacional:** no ambiente Windows, ficheiros `.wav` em `prep/data` apareceram com **0 bytes** (placeholders). O treino utilizou **tokens semânticos** pré-extraídos (`segment_*.npy`). Na inferência, o prompt de referência foi obtido a partir de `segment_1.npy` (decodificado para `reference_prompt.wav`).

---

## Hiperparâmetros de treino

| Hiperparâmetro | Valor |
|----------------|--------|
| `trainer.max_steps` | **10 488** |
| Número de épocas sintéticas | **1** |
| `data.batch_size` | **4** |
| `trainer.accumulate_grad_batches` | **1** |
| Amostras efetivas por passo | **4** |
| `model.optimizer.lr` | **1×10⁻⁴** |
| Otimizador | AdamW, β=(0,9; 0,95), ε=1×10⁻⁵ |
| Warmup | **10** steps |
| `max_length` (tokens/texto) | **4096** |
| `data.num_workers` | **0** |
| `trainer.precision` | bf16-true |
| `trainer.devices` | **1** GPU |
| `trainer.log_every_n_steps` | **5** |
| `trainer.val_check_interval` | **10 488** (validação no fim da época) |
| `trainer.limit_val_batches` | **32** |
| `trainer.gradient_clip_val` | **1,0** (norm) |
| Checkpoint | `every_n_train_steps=10488`, `save_top_k=1` |
| `interactive_prob` (dataset) | **0,7** |
| `use_speaker` | **false** |

Configuração completa: `config/hparams.yaml`.

---

## Ambiente de execução

| Item | Valor |
|------|--------|
| SO (container) | Linux (WSL2 kernel 6.6.87) |
| Python | 3.11.10 |
| PyTorch | 2.5.1+cu124 (CUDA 12.4) |
| GPU | **NVIDIA GeForce RTX 4060 Ti** (1×) |
| CPU lógicos | 12 |
| RAM (container) | ~16 GiB |

Detalhes: `config/machine_profile.json`.

---

## Resultados numéricos do treino

| Métrica | Valor |
|---------|--------|
| Duração de parede (span entre logs TensorBoard) | **~44,7 h** (~160 996 s) |
| Intervalo médio entre logs de treino | **~76,8 s** |
| Passos com log (`train/loss`) | **4 … 10 484** (2097 pontos) |
| `train/loss` no passo 4 | **9,50** |
| `train/loss` no passo 10 484 | **8,88** |
| Média `train/loss` (época sintética 1) | **9,026** |
| Mínimo / máximo `train/loss` observados | **8,56** / **9,69** |
| `val/loss` (passo 10 487) | **8,963** |

**Tags TensorBoard registadas:** `train/loss`, `train/base_loss`, `train/semantic_loss`, `train/grad_norm`, `train/top_5_accuracy`, `val/loss`, `val/base_loss`, `val/semantic_loss`, `val/top_5_accuracy`, `lr-AdamW/pg1`, `lr-AdamW/pg2`.

**Interpretação:** em uma época sintética, a perda de treino desce de forma **modesta** (9,50 → 8,88; média 9,03). O `val/loss` final (8,96) está próximo da média de treino; com um único ponto de validação no fim da época, não há evidência forte de overfitting.

**Estado do pipeline:** o treino Lightning **concluiu** e o checkpoint foi gravado. A fase pós-treino inicial falhou por scripts com CRLF no Windows; foi **reexecutada com sucesso** (`SKIP_TRAIN=1`).

**Ficheiros de métricas:** `metrics/train_loss_by_step.csv`, `metrics/eval_loss_by_step.csv`, `metrics/train_loss_synthetic_epoch.csv`, `metrics/eval_loss_synthetic_epoch.csv`, `metrics/timing_summary.json`, `metrics/training_wall_time_between_logged_steps.csv`, `metrics/estimated_train_wall_seconds_per_synthetic_epoch.csv`.

**Gráficos:** `plots/train_loss_by_step.png`, `plots/val_loss_by_step.png`, `plots/train_loss_mean_by_epoch.png`, `plots/eval_loss_mean_by_epoch.png`, `plots/estimated_train_seconds_by_epoch.png`. Gráfico com estilo unificado da documentação: `../outputs/grafico_perda_ajuste_fino_fishspeech_por_passo.png`.

---

## Protocolo de inferência

| Item | Valor |
|------|--------|
| Frases de teste | 5 linhas em pt-BR |
| Dispositivo | CUDA |
| Prompt de referência | `segment_1` → transcrição + tokens `segment_1.npy` |
| Baseline | Modelo `fish-speech-1.5` **sem** merge LoRA |
| Fine-tuned | Merge LoRA de `step_000010488.ckpt` + `generate.py` + decode VQGAN |

### Transcrição do prompt de referência

```
eu sou muito fácil para conseguir amizades. então, eu tenho amizades em brasília, em belo horizonte...
```

### Cinco frases de síntese (pt-BR)

1. Hoje acordei cedo, preparei um café forte e organizei a mesa para estudar com calma.
2. Enquanto o trem passava devagar, uma criança sorria e apontava para as nuvens alaranjadas.
3. O pesquisador analisou os dados, escreveu um relatório objetivo e compartilhou as conclusões com a equipe.
4. Estamos construindo uma rotina mais saudável, caminhando no bairro e cozinhando alimentos frescos todos os dias.
5. A bibliotecária catalogou romances, dicionários e biografias, mantendo cada prateleira limpa e bem sinalizada.

### Áudios deste experimento

| Condição | Ficheiros |
|----------|-----------|
| Prompt de referência | `audio/reference/reference_prompt.wav` |
| Baseline (pré-treinado) | `audio/baseline_pretrained/baseline_phrase_01.wav` … `05.wav` |
| Fine-tuned (step 10 488) | `audio/inference_finetuned/step_000010488_phrase_01.wav` … `05.wav` |

### Tabela para avaliação perceptiva (preencher após escuta)

| # | Frase (resumo) | Baseline | Fine-tuned | Observação |
|---|----------------|----------|------------|------------|
| 1 | Café / estudar | `baseline_phrase_01.wav` | `step_000010488_phrase_01.wav` | |
| 2 | Trem / criança | `baseline_phrase_02.wav` | `step_000010488_phrase_02.wav` | |
| 3 | Pesquisador / relatório | `baseline_phrase_03.wav` | `step_000010488_phrase_03.wav` | |
| 4 | Rotina saudável | `baseline_phrase_04.wav` | `step_000010488_phrase_04.wav` | |
| 5 | Bibliotecária | `baseline_phrase_05.wav` | `step_000010488_phrase_05.wav` | |

**Atenção:** ficheiros `output/synthesized_speech_phrase_*.wav` (scripts `run_inference.bat` / `inference_demo.sh`) usam **apenas o modelo base** e **não** pertencem a este checkpoint fine-tuned.

Manifesto: `config/listening_comparison_manifest.json` · Frases: `config/inference_phrases_ptbr.txt`.

---

## Estrutura da pasta `output_experiments/`

```
output_experiments/
├── relatorio.md
├── relatorio_dissertacao_prompt.md    ← este ficheiro
├── checkpoint/step_000010488.ckpt
├── config/
│   ├── hparams.yaml
│   ├── dataset_stats.json
│   ├── dataset_text_stats.json
│   ├── machine_profile.json
│   ├── inference_phrases_ptbr.txt
│   ├── reference_prompt_transcript.txt
│   └── listening_comparison_manifest.json
├── metrics/          ← CSVs e JSON de perdas e tempos
├── plots/            ← gráficos PNG
└── audio/
    ├── reference/
    ├── baseline_pretrained/
    └── inference_finetuned/
```

---

## Texto corrido para a dissertação (apenas Fish Speech)

Foi realizado fine-tuning **LoRA** (r=8, α=16) sobre o **Fish Speech 1.5** (`fishaudio/fish-speech-1.5`), no módulo **text2semantic**, com corpus **Paraíba** (`filtered_char`): 41 952 segmentos em português brasileiro (~44,8 h de fala), speaker `PB_PARAIBA`. O treino limitou-se a **10 488** passos de otimização (uma época sintética, batch efetivo 4, learning rate 10⁻⁴, precisão bf16), em **uma GPU NVIDIA RTX 4060 Ti**, com duração de parede da ordem de **45 horas**. Apenas **0,96%** dos parâmetros foram atualizados; o checkpoint LoRA final ocupa cerca de **36 MiB**. A perda de treino média na época foi **9,03** (passos inicial e final: **9,50** e **8,88**); a perda de validação no passo **10 487** foi **8,96**. A avaliação perceptiva comparou sínteses do modelo pré-treinado e do modelo com LoRA fundido no passo **10 488**, com cinco frases em pt-BR e o mesmo prompt de voz (segmento 1 do corpus, reconstruído a partir de tokens semânticos). Limitações desta rodada: uma única época sintética; validação apenas no fim do treino; ausência de métricas automáticas de qualidade de síntese (MOS, WER, NISQA) neste pacote; WAVs do corpus não materializados no disco Windows durante o pós-processamento.

---

## Limitações deste experimento (Fish Speech)

1. **Uma época sintética** — treino interrompido pelo orçamento de GPU/tempo (~45 h de parede).
2. **Validação pontual** — um único `val/loss` no passo 10 487.
3. **Treino em tokens `.npy`** — WAVs com 0 bytes no ambiente Windows; prompt via reconstrução VQGAN.
4. **Sem métricas objetivas de síntese** neste pacote — apenas curvas de loss e comparação auditiva baseline vs. fine-tuned.
5. **Pós-processamento** — falha inicial por CRLF; conclusão com `SKIP_TRAIN=1`.

---

## Instrução sugerida para o outro prompt

```
Com base APENAS no documento acima (fine-tuning Fish Speech 1.5, experimento paraiba_20260510_031412),
redija [Métodos / Resultados / Discussão] em português académico (PT-BR).
Não compare com outros modelos TTS. Não invente métricas que não constam no documento.
Use as tabelas e números fornecidos. Para avaliação perceptiva, use [PREENCHER APÓS ESCUTA].
```

---

*Exportação · `docs/17/fishspeech/output_experiments/relatorio_dissertacao_prompt.md`*
