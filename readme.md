# Projeto de Síntese de Fala (Mestrado)

Este repositório acompanha o progresso do meu projeto de mestrado em Ciência da Computação, cujo objetivo é realizar **fine-tuning** de modelos de Text-to-Speech (TTS) para síntese de fala em Português. Aqui você encontrará instruções de uso, scripts auxiliares e exemplos de áudios gerados com **Coqui TTS** e **F5-TTS**.

https://thomazdiniz.github.io/fala_pb/
https://thomazdiniz.github.io/fala_pb/2

---

## 📁 Estrutura do repositório

- **docs/**: arquivos da GitHub Pages. Habilite em **Settings → Pages** apontando para `branch: main` e pasta `/docs`.  
- **scripts/**: facilita repetir comandos Docker sem digitar tudo manualmente.  
- **outputs/**: onde você gera os `.wav` localmente (adicione em `.gitignore`).  
- **docs/audio/**: exemplos públicos de áudio para mostrar na página.


## Rodando o COQUI_AI para sintetizar vozes no docker

``` 
	mkdir E:\tts_output
	mkdir E:\coqui tts cache

	CPU:
	docker pull ghcr.io/coqui-ai/tts-cpu:latest

	GPU:
	docker pull ghcr.io/coqui-ai/tts:latest

	//listar modelos:
	docker run --rm -it `
	  --gpus all `
	  -v "E:\coqui tts cache:/root/.cache/tts" `
	  ghcr.io/coqui-ai/tts:latest `
	    --list_models




	//listar speakers do xtts ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski'])

	docker run --rm -it `
	  --gpus all `
	  -e TTS_HOME=/root/.cache/tts `
	  -v "E:\coqui tts cache:/root/.cache/tts" `
	  ghcr.io/coqui-ai/tts:latest `
	    --model_name tts_models/multilingual/multi-dataset/xtts_v2 `
	    --list_speaker_idxs


# Listar os modelos
docker run --rm -it `
  --gpus all `
  -e TTS_HOME=/root/.cache/tts `
  -v "E:\coqui tts cache:/root/.cache/tts" `
  ghcr.io/coqui-ai/tts:latest `
    --list_models




# gerar falas de fato

	docker run --rm -it `
	  --gpus all `
	  -e TTS_HOME=/root/.cache/tts `
	  -v "E:\coqui tts cache:/root/.cache/tts" `
	  -v "E:\tts_output:/output" `
	  ghcr.io/coqui-ai/tts:latest `
	    --model_name tts_models/multilingual/multi-dataset/xtts_v2 `
	    --speaker_idx 'Luis Moray' `
	    --language_idx pt `
	    --text "Eu te amo" `
	    --out_path /output/xtts_cached.wav

```



## Rodando o F5TTS no docker
```
mkdir E:\f5tts_cache

docker pull ghcr.io/swivid/f5-tts:main

docker run --rm -it `
  --gpus all `
  --mount type=bind,source=E:\f5tts_cache,target=/root/.cache/huggingface/hub `
  -p 7860:7860 `
  ghcr.io/swivid/f5-tts:main `
    f5-tts_infer-gradio --host 0.0.0.0


#acesse: http://localhost:7860/
```


# F5TTS PTBR

```
docker run --rm -it `
  --gpus all `
  --mount "type=bind,source=C:/Users/Tumais/Documents/GitHub/F5-TTS-pt-br/pt-br,target=/root/.cache/huggingface/hub/models--firstpixel--F5-TTS-pt-br,readonly" `
  -p 7860:7860 `
  ghcr.io/swivid/f5-tts:main `
  f5-tts_infer-gradio --host 0.0.0.0

docker run --rm -it --gpus all `
  --mount "type=bind,source=C:/Users/Tumais/Documents/GitHub/F5-TTS-pt-br,target=/root/.cache/huggingface/hub/models--firstpixel--F5-TTS-pt-br,readonly" `
  -p 7860:7860 `
  ghcr.io/swivid/f5-tts:main `
  f5-tts_infer-gradio --host 0.0.0.0
  
```



```
C:\Users\Tumais\Documents\GitHub\F5-TTS-pt-br\pt-br\model_last.safetensors
C:\Users\Tumais\Documents\GitHub\F5-TTS-pt-br\pt-br\model_last.pt
C:\Users\Tumais\Documents\GitHub\F5-TTS-pt-br\pt-br\model_200000.pt
```
