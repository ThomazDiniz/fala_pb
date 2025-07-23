# 1) Defina aqui suas 10 sentenças de teste
$sentences = @(
  "Olá, tudo bem?",
  "A vida é feita de escolhas.",
  "Aprender nunca é demais.",
  "Hoje o céu amanheceu com nuvens carregadas e uma leve brisa.",
  "A tecnologia mudou a forma como nos comunicamos e aprendemos.",
  "No interior da cidade, praças antigas guardam histórias de gerações.",
  "O café fresco pela manhã anima qualquer rotina.",
  "Em um mundo cada vez mais conectado, é fundamental equilibrar o uso de dispositivos móveis com momentos de descanso e socialização presencial, preservando nossa saúde mental e bem‑estar.",
  "As bibliotecas públicas têm papel essencial na democratização do conhecimento, oferecendo não só livros, mas também acesso à internet, cursos e espaços de convivência para a comunidade local.",
  "Projetos de ciência cidadã estimulam a participação de voluntários em coletas de dados ambientais e podem contribuir para pesquisas sobre mudanças climáticas, flora, fauna e qualidade da água em diversas regiões."
)

# 2) Defina os 3 grupos de referências com seus paths dentro do container
$groups = @(
  @{ Key = 'A'; Files = @(
        "/refs/thomaz_a1.wav", "/refs/thomaz_a2.wav",
        "/refs/thomaz_a3.wav", "/refs/thomaz_a4.wav",
        "/refs/thomaz_a5.wav"
    )
  },
  @{ Key = 'B'; Files = @(
        "/refs/thomaz_b1.wav", "/refs/thomaz_b2.wav",
        "/refs/thomaz_b3.wav", "/refs/thomaz_b4.wav",
        "/refs/thomaz_b5.wav"
    )
  },
  @{ Key = 'C'; Files = @(
        "/refs/thomaz_c1.wav", "/refs/thomaz_c2.wav",
        "/refs/thomaz_c3.wav", "/refs/thomaz_c4.wav",
        "/refs/thomaz_c5.wav"
    )
  }
)

# 3) Loop principal: para cada grupo e cada sentença, gera um WAV
foreach ($group in $groups) {
  $tag   = $group.Key
  $files = $group.Files

  foreach ($sent in $sentences) {
    # gerar nome "seguro" para o arquivo de saída
    $safeSent = ($sent -replace '[^0-9A-Za-zÀ-ú ]','') -replace ' ','_'
    $outFile  = "/output/xtts_${tag}_${safeSent}.wav"

    Write-Host "[$tag] Gerando: $outFile"

    docker run --rm -it `
      --gpus all `
      -e TTS_HOME=/root/.cache/tts `
      -v "E:/coqui tts cache:/root/.cache/tts" `
      -v "E:/tts_output:/output" `
      -v "E:/tts_refs:/refs" `
      ghcr.io/coqui-ai/tts:latest `
        --model_name tts_models/multilingual/multi-dataset/xtts_v2 `
        --speaker_wav $($files[0]) $($files[1]) $($files[2]) $($files[3]) $($files[4]) `
        --language_idx pt `
        --text "$sent" `
        --out_path "$outFile"
  }
}