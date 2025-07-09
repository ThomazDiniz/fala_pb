---
title: Fala PB
---

# Demonstrações de Síntese de Fala

## Coqui TTS

| Speaker      | Exemplo                           |
|--------------|-----------------------------------|
| Luis Moray   | <audio controls src="audio/coqui/example1.wav"></audio> |
| Ana Florence | <audio controls src="audio/coqui/example2.wav"></audio> |

## F5-TTS

| Descrição         | Exemplo                                   |
|-------------------|-------------------------------------------|
| Gradio inferência | <audio controls src="audio/f5tts/example1.wav"></audio> |
| Pipeline autônomo | <audio controls src="audio/f5tts/example2.wav"></audio> |

# Registro de Experimentos TTS

Este documento reúne todos os experimentos e reuniões em ordem **decrescente** de data. Use o sumário abaixo para navegar diretamente até cada seção.

## Sumário

- [📅 Reunião 2025-08-01: Último Experimento](#reunião-2025-08-01-último-experimento)  
- [📅 Reunião 2025-07-15: Fine-Tuning Inicial](#reunião-2025-07-15-fine-tuning-inicial)  
- [📅 Reunião 2025-07-01: Configuração Inicial](#reunião-2025-07-01-configuração-inicial)  

---

<a name="reunião-2025-08-01-último-experimento"></a>
## 📅 Reunião 2025-08-01: Último Experimento

**Data:** 1º de agosto de 2025  
**Ata de referência:** [Link para o documento](https://docs.google.com/document/d/1y5N87dHTs5kF3Iz002LUX5LNS120k5FxvuSFlrQAhWE/edit?tab=t.0)

### Resumo
Nesta reunião finalizamos o pipeline de fine-tuning no Coqui TTS, testamos três novos valores de learning rate e coletamos exemplos de áudio para comparação.

### Exemplos de Áudio
- **Coqui TTS (Luis Moray):**  
  <audio controls src="audio/coqui/exp-2025-08-01-luis_moray.wav"></audio>  
- **F5-TTS (Pipeline autônomo):**  
  <audio controls src="audio/f5tts/exp-2025-08-01-pipeline.wav"></audio>

### Próximos Passos
1. Gerar relatório de métricas de naturalidade (MOS).  
2. Planejar publicação de paper.  

---

<a name="reunião-2025-07-15-fine-tuning-inicial"></a>
## 📅 Reunião 2025-07-15: Fine-Tuning Inicial

**Data:** 15 de julho de 2025  
**Ata de referência:** [Link para o documento](https://docs.google.com/document/d/1y5N87dHTs5kF3Iz002LUX5LNS120k5FxvuSFlrQAhWE/edit?tab=t.0)

### Resumo
Discutimos os resultados dos primeiros 5 epochs de fine-tuning no F5-TTS e definimos as métricas de avaliação.

### Exemplos de Áudio
- **Coqui TTS (Ana Florence):**  
  <audio controls src="audio/coqui/exp-2025-07-15-ana_florence.wav"></audio>  
- **F5-TTS (Gradio inferência):**  
  <audio controls src="audio/f5tts/exp-2025-07-15-gradio.wav"></audio>

### Próximos Passos
1. Ajustar taxa de aprendizado para 1e-4.  
2. Automatizar geração de gráficos de perda.  

---

<a name="reunião-2025-07-01-configuração-inicial"></a>
## 📅 Reunião 2025-07-01: Configuração Inicial

**Data:** 1º de julho de 2025  
**Ata de referência:** [Link para o documento](https://docs.google.com/document/d/1y5N87dHTs5kF3Iz002LUX5LNS120k5FxvuSFlrQAhWE/edit?tab=t.0)

### Resumo
Definimos a estrutura do repositório, criamos scripts Docker para Coqui TTS e F5-TTS, e organizamos onde armazenar os áudios de exemplo.

### Exemplos de Áudio
- **Coqui TTS (Luis Moray):**  
  <audio controls src="audio/coqui/example1.wav"></audio>  
- **F5-TTS (Gradio inferência):**  
  <audio controls src="audio/f5tts/example1.wav"></audio>

### Próximos Passos
1. Listar todos os modelos disponíveis (`--list_models`).  
2. Testar `--list_speaker_idxs` no XTTS.  

---

> Sempre que adicionar uma nova reunião, inclua-a **no topo** do sumário e crie a seção correspondente abaixo.
