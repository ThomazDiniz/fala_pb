import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

device = "cuda:0" if torch.cuda.is_available() else "cpu"
#Claro\! O resultado da execução do código, que cria a lista a partir dos nomes do dicionário, é:

speakers = ['Diana', 'Eduardo', 'Uriel', 'Guilherme', 'Zoe', 'Quirino', 'Enzo', 'Henrique', 'Davi', 'Thiago', 'Sofia', 'Wilson', 'Ximenia', 'Osvaldo', 'Icaro', 'Raquel', 'Carolina', 'Debora', 'Xavier', 'Olivia', 'Erick', 'Silvio', 'Daniel', 'Joao', 'Italo', 'Manuela', 'Caio', 'Yuri', 'Samuel', 'Isabela', 'Sabrina', 'Paulo', 'Victor', 'Amanda', 'Alexandre', 'Vitoria', 'Emilia', 'Diego', 'Daniela', 'Joana', 'Gabriel', 'Wanda', 'Alice', 'Valentina', 'Bruno', 'Hugo', 'Yara', 'Vinicius', 'Patricia', 'Luiz', 'Valter', 'Leticia', 'Iris', 'Fernando', 'Julio', 'Carlos', 'Lucas', 'Mateus', 'Rebeca', 'Rafael', 'Bernardo', 'Flavia']

model = ParlerTTSForConditionalGeneration.from_pretrained("freds0/parler-tts-mini-v1.1-ptbr").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-multilingual")
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

prompt = "Eu gostaria mesmo é estar comendo uma buchada de bode na minha terrinha distante."
description = "Eduardo's speech is very clear and has a consistent tone, his accent is from brazils northeast and he is in a very confined sounding environment with clear audio quality."

input_ids = description_tokenizer(description, return_tensors="pt").input_ids.to(device)
prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
audio_arr = generation.cpu().numpy().squeeze()
sf.write("parler_tts_out.wav", audio_arr, model.config.sampling_rate)
