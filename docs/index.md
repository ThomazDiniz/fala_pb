---
title: Fala PB
---

<style>
  .wrapper,
  .markdown-body, .inner, #main_content {
    max-width: 90% !important;
    padding: 1rem 2rem !important;
  }

</style>

# Retomando experimentos com Síntese de Fala

O foco nesta seção é retomar experimentos iniciais de síntese de fala utilizando o docker.  


## Coqui AI
Nesta seção retomamos a parte do coqui AI, já há um experimento com exemplos do coqui ai.

### Português Brasileiro

**tts_models/multilingual/multi-dataset/xtts_v2**  
Suporta 16 idiomas, incluindo o português brasileiro (“pt”), usando embeddings de idioma e de falante para geração zero-shot com alta fidelidade na prosódia e entonação.

**tts_models/multilingual/multi-dataset/xtts_v1.1**  
Cobre 14 idiomas, entre eles “pt”, com uma versão otimizada do Transformer-TTS que oferece síntese expressiva em pt-BR, ideal para protótipos e testes rápidos.

**tts_models/multilingual/multi-dataset/your_tts**  
Treinado com o TTS-Portuguese Corpus (TPC) para português brasileiro, baseado em VITS com adversarial learning, garantindo naturalidade, clareza e variedade de entonações típicas do pt-BR.

### Português de Portugal

**tts_models/pt/cv/vits**  
Modelo VITS exclusivo para português europeu (pt-PT), treinado no Common Voice, que entrega voz articulada e ritmo consistente, perfeito para público de Portugal.  

<details>
<summary>Lista de modelos disponíveis pelo coqui ai</summary>
 Name format: type/language/dataset/model
 1: tts_models/multilingual/multi-dataset/xtts_v2
 2: tts_models/multilingual/multi-dataset/xtts_v1.1
 3: tts_models/multilingual/multi-dataset/your_tts
 4: tts_models/multilingual/multi-dataset/bark
 5: tts_models/bg/cv/vits
 6: tts_models/cs/cv/vits
 7: tts_models/da/cv/vits
 8: tts_models/et/cv/vits
 9: tts_models/ga/cv/vits
 10: tts_models/en/ek1/tacotron2
 11: tts_models/en/ljspeech/tacotron2-DDC
 12: tts_models/en/ljspeech/tacotron2-DDC_ph
 13: tts_models/en/ljspeech/glow-tts
 14: tts_models/en/ljspeech/speedy-speech
 15: tts_models/en/ljspeech/tacotron2-DCA
 16: tts_models/en/ljspeech/vits
 17: tts_models/en/ljspeech/vits--neon
 18: tts_models/en/ljspeech/fast_pitch
 19: tts_models/en/ljspeech/overflow
 20: tts_models/en/ljspeech/neural_hmm
 21: tts_models/en/vctk/vits
 22: tts_models/en/vctk/fast_pitch
 23: tts_models/en/sam/tacotron-DDC
 24: tts_models/en/blizzard2013/capacitron-t2-c50
 25: tts_models/en/blizzard2013/capacitron-t2-c150_v2
 26: tts_models/en/multi-dataset/tortoise-v2
 27: tts_models/en/jenny/jenny
 28: tts_models/es/mai/tacotron2-DDC
 29: tts_models/es/css10/vits
 30: tts_models/fr/mai/tacotron2-DDC
 31: tts_models/fr/css10/vits
 32: tts_models/uk/mai/glow-tts
 33: tts_models/uk/mai/vits
 34: tts_models/zh-CN/baker/tacotron2-DDC-GST
 35: tts_models/nl/mai/tacotron2-DDC
 36: tts_models/nl/css10/vits
 37: tts_models/de/thorsten/tacotron2-DCA
 38: tts_models/de/thorsten/vits
 39: tts_models/de/thorsten/tacotron2-DDC
 40: tts_models/de/css10/vits-neon
 41: tts_models/ja/kokoro/tacotron2-DDC
 42: tts_models/tr/common-voice/glow-tts
 43: tts_models/it/mai_female/glow-tts
 44: tts_models/it/mai_female/vits
 45: tts_models/it/mai_male/glow-tts
 46: tts_models/it/mai_male/vits
 47: tts_models/ewe/openbible/vits
 48: tts_models/hau/openbible/vits
 49: tts_models/lin/openbible/vits
 50: tts_models/tw_akuapem/openbible/vits
 51: tts_models/tw_asante/openbible/vits
 52: tts_models/yor/openbible/vits
 53: tts_models/hu/css10/vits
 54: tts_models/el/cv/vits
 55: tts_models/fi/css10/vits
 56: tts_models/hr/cv/vits
 57: tts_models/lt/cv/vits
 58: tts_models/lv/cv/vits
 59: tts_models/mt/cv/vits
 60: tts_models/pl/mai_female/vits
 61: tts_models/pt/cv/vits
 62: tts_models/ro/cv/vits
 63: tts_models/sk/cv/vits
 64: tts_models/sl/cv/vits
 65: tts_models/sv/cv/vits
 66: tts_models/ca/custom/vits
 67: tts_models/fa/custom/glow-tts
 68: tts_models/bn/custom/vits-male
 69: tts_models/bn/custom/vits-female
 70: tts_models/be/common-voice/glow-tts

 Name format: type/language/dataset/model
 1: vocoder_models/universal/libri-tts/wavegrad
 2: vocoder_models/universal/libri-tts/fullband-melgan
 3: vocoder_models/en/ek1/wavegrad
 4: vocoder_models/en/ljspeech/multiband-melgan
 5: vocoder_models/en/ljspeech/hifigan_v2
 6: vocoder_models/en/ljspeech/univnet
 7: vocoder_models/en/blizzard2013/hifigan_v2
 8: vocoder_models/en/vctk/hifigan_v2
 9: vocoder_models/en/sam/hifigan_v2
 10: vocoder_models/nl/mai/parallel-wavegan
 11: vocoder_models/de/thorsten/wavegrad
 12: vocoder_models/de/thorsten/fullband-melgan
 13: vocoder_models/de/thorsten/hifigan_v1
 14: vocoder_models/ja/kokoro/hifigan_v1
 15: vocoder_models/uk/mai/multiband-melgan
 16: vocoder_models/tr/common-voice/hifigan
 17: vocoder_models/be/common-voice/hifigan
</details>


## Tabela de Áudios XTTS 
Nesta tabela temos todos os speakers possiveis falando a frase "Eu te amo". Também é [possível fazer few shot que fiz com 5 audios usando minha própria voz](https://thomazdiniz.github.io/tts/):

| Speaker             | Exemplo                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------|
| Abrahan Mack        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Abrahan_Mack.wav"></audio>                 |
| Aaron Dreschner     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Aaron_Dreschner.wav"></audio>              |
| Adde Michal         | <audio controls src="audios/xtts2/Eu_te_amo_pt_Adde_Michal.wav"></audio>                  |
| Alison Dietlinde    | <audio controls src="audios/xtts2/Eu_te_amo_pt_Alison_Dietlinde.wav"></audio>             |
| Alexandra Hisakawa  | <audio controls src="audios/xtts2/Eu_te_amo_pt_Alexandra_Hisakawa.wav"></audio>           |
| Alma María          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Alma_María.wav"></audio>                   |
| Andrew Chipper      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Andrew_Chipper.wav"></audio>               |
| Ana Florence        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Ana_Florence.wav"></audio>                 |
| Annmarie Nele       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Annmarie_Nele.wav"></audio>                |
| Asya Anara          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Asya_Anara.wav"></audio>                   |
| Badr Odhiambo       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Badr_Odhiambo.wav"></audio>                |
| Barbora MacLean     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Barbora_MacLean.wav"></audio>             |
| Baldur Sanjin       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Baldur_Sanjin.wav"></audio>                |
| Brenda Stern        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Brenda_Stern.wav"></audio>                 |
| Camilla Holmström   | <audio controls src="audios/xtts2/Eu_te_amo_pt_Camilla_Holmström.wav"></audio>           |
| Chandra MacFarland  | <audio controls src="audios/xtts2/Eu_te_amo_pt_Chandra_MacFarland.wav"></audio>          |
| Claribel Dervla     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Claribel_Dervla.wav"></audio>              |
| Craig Gutsy         | <audio controls src="audios/xtts2/Eu_te_amo_pt_Craig_Gutsy.wav"></audio>                  |
| Damien Black        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Damien_Black.wav"></audio>                 |
| Damjan Chapman      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Damjan_Chapman.wav"></audio>              |
| Daisy Studious      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Daisy_Studious.wav"></audio>               |
| Dionisio Schuyler   | <audio controls src="audios/xtts2/Eu_te_amo_pt_Dionisio_Schuyler.wav"></audio>            |
| Eugenio Mataracı    | <audio controls src="audios/xtts2/Eu_te_amo_pt_Eugenio_Mataracı.wav"></audio>           |
| Ferran Simen        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Ferran_Simen.wav"></audio>                |
| Filip Traverse      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Filip_Traverse.wav"></audio>              |
| Gilberto Mathias    | <audio controls src="audios/xtts2/Eu_te_amo_pt_Gilberto_Mathias.wav"></audio>             |
| Gitta Nikolina      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Gitta_Nikolina.wav"></audio>               |
| Henriette Usha      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Henriette_Usha.wav"></audio>               |
| Ilkin Urbano        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Ilkin_Urbano.wav"></audio>                 |
| Ige Behringer       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Ige_Behringer.wav"></audio>               |
| Kumar Dahl          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Kumar_Dahl.wav"></audio>                  |
| Kazuhiko Atallah    | <audio controls src="audios/xtts2/Eu_te_amo_pt_Kazuhiko_Atallah.wav"></audio>             |
| Lidiya Szekeres     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Lidiya_Szekeres.wav"></audio>             |
| Lilya Stainthorpe   | <audio controls src="audios/xtts2/Eu_te_amo_pt_Lilya_Stainthorpe.wav"></audio>           |
| Ludvig Milivoj      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Ludvig_Milivoj.wav"></audio>               |
| Maja Ruoho          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Maja_Ruoho.wav"></audio>                  |
| Marcos Rudaski      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Marcos_Rudaski.wav"></audio>              |
| Nova Hogarth        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Nova_Hogarth.wav"></audio>                |
| Narelle Moon        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Narelle_Moon.wav"></audio>                |
| Rosemary Okafor     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Rosemary_Okafor.wav"></audio>             |
| Royston Min         | <audio controls src="audios/xtts2/Eu_te_amo_pt_Royston_Min.wav"></audio>                  |
| Sofia Hellen        | <audio controls src="audios/xtts2/Eu_te_amo_pt_Sofia_Hellen.wav"></audio>                 |
| Suad Qasim          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Suad_Qasim.wav"></audio>                   |
| Szofi Granger       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Szofi_Granger.wav"></audio>               |
| Tammie Ema          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Tammie_Ema.wav"></audio>                   |
| Tammy Grit          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Tammy_Grit.wav"></audio>                   |
| Tanja Adelina       | <audio controls src="audios/xtts2/Eu_te_amo_pt_Tanja_Adelina.wav"></audio>                |
| Torcull Diarmuid    | <audio controls src="audios/xtts2/Eu_te_amo_pt_Torcull_Diarmuid.wav"></audio>             |
| Uta Obando          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Uta_Obando.wav"></audio>                  |
| Viktor Eka          | <audio controls src="audios/xtts2/Eu_te_amo_pt_Viktor_Eka.wav"></audio>                   |
| Viktor Menelaos     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Viktor_Menelaos.wav"></audio>              |
| Vjollca Johnnie     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Vjollca_Johnnie.wav"></audio>              |
| Wulf Carlevaro      | <audio controls src="audios/xtts2/Eu_te_amo_pt_Wulf_Carlevaro.wav"></audio>              |
| Xavier Hayasaka     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Xavier_Hayasaka.wav"></audio>             |
| Zacharie Aimilios   | <audio controls src="audios/xtts2/Eu_te_amo_pt_Zacharie_Aimilios.wav"></audio>            |
| Zofija Kendrick     | <audio controls src="audios/xtts2/Eu_te_amo_pt_Zofija_Kendrick.wav"></audio>             |


## F5-TTS

| Descrição         | Exemplo                                   |
|-------------------|-------------------------------------------|
| Gradio inferência | <audio controls src="audio/f5tts/example1.wav"></audio> |
| Pipeline autônomo | <audio controls src="audio/f5tts/example2.wav"></audio> |





<!--
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

-->