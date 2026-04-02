---
title: "Experimento FINETUNE F5TTS 3 — Áudios"
permalink: /11-audios/
layout: default
---

<style>
  .wrapper,
  .markdown-body, .inner, #main_content {
    max-width: 90% !important;
    padding: 1rem 2rem !important;
  }
  .markdown-body table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1rem;
  }
  .markdown-body th,
  .markdown-body td {
    border: 1px solid #ccc;
    padding: 0.5rem;
    vertical-align: top;
  }
  .markdown-body th {
    background: #f5f5f5;
    text-align: left;
  }
  audio {
    width: 100%;
    min-width: 260px;
  }
  .muted {
    color: #666;
  }
</style>

# Experimento FINETUNE F5TTS 3 — Áudios

Relatório do experimento: **[voltar](/fala_pb/11/)**.

Nesta página, cada treino tem:

- Uma tabela **Texto | Áudio** (inferência)
- Uma tabela **Ref | Gen** (checkpoints)

## Treino `brpb22_g1bf01`

### Inferência

| Texto | Áudio |
|---|---|
| Eu estava pensando em passar ali na feira antes de ir pra casa. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/inferencia/1.wav"></audio> |
| Visse, esse menino não para quieto nem um segundo. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/inferencia/2.wav"></audio> |
| Bota mais agua nesse café que ficou forte demais. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/inferencia/3.wav"></audio> |

### Checkpoints (Ref | Gen)

| Step | Ref | Gen |
|---:|---|---|
| 250 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_250_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_250_gen.wav"></audio> |
| 500 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_500_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_500_gen.wav"></audio> |
| 750 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_750_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_750_gen.wav"></audio> |
| 1000 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_1000_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_1000_gen.wav"></audio> |
| 1250 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_1250_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brpb22_g1bf01/step_1250_gen.wav"></audio> |

## Treino `brPB01_g2aF01`

### Inferência

| Texto | Áudio |
|---|---|
| Eu estava pensando em passar ali na feira antes de ir pra casa. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/inferencia/1.wav"></audio> |
| Visse, esse menino não para quieto nem um segundo. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/inferencia/2.wav"></audio> |
| Bota mais agua nesse café que ficou forte demais. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/inferencia/3.wav"></audio> |

### Checkpoints (Ref | Gen)

| Step | Ref | Gen |
|---:|---|---|
| 300 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_300_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_300_gen.wav"></audio> |
| 600 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_600_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_600_gen.wav"></audio> |
| 900 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_900_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_900_gen.wav"></audio> |
| 1200 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1200_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1200_gen.wav"></audio> |
| 1500 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1500_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1500_gen.wav"></audio> |
| 1800 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1800_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_1800_gen.wav"></audio> |
| 2100 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2100_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2100_gen.wav"></audio> |
| 2400 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2400_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2400_gen.wav"></audio> |
| 2700 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2700_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_2700_gen.wav"></audio> |
| 3000 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3000_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3000_gen.wav"></audio> |
| 3300 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3300_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3300_gen.wav"></audio> |
| 3600 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3600_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3600_gen.wav"></audio> |
| 3900 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3900_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_3900_gen.wav"></audio> |
| 4200 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4200_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4200_gen.wav"></audio> |
| 4500 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4500_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4500_gen.wav"></audio> |
| 4800 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4800_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_4800_gen.wav"></audio> |
| 5100 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_5100_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/brPB01_g2aF01/step_5100_gen.wav"></audio> |

## Treino `all`

### Inferência

| Texto | Áudio |
|---|---|
| Eu estava pensando em passar ali na feira antes de ir pra casa. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/inferencia/1.wav"></audio> |
| Visse, esse menino não para quieto nem um segundo. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/inferencia/2.wav"></audio> |
| Bota mais agua nesse café que ficou forte demais. | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/inferencia/3.wav"></audio> |

### Checkpoints (Ref | Gen)

| Step | Ref | Gen |
|---:|---|---|
| 221705 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/step_221705_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/step_221705_gen.wav"></audio> |
| 443410 | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/step_443410_ref.wav"></audio> | <audio controls src="../audios/Experimento%20FINETUNE%20F5TTS%203/all/step_443410_gen.wav"></audio> |

<p class="muted">Obs.: os textos estão em <code>inferencia/txt.txt</code> em cada pasta.</p>

