# generate_xtts_speakers.ps1
# Script que gera um arquivo WAV com a mensagem para cada speaker do modelo xtts_v2
# Usa --speaker e --language conforme CLI correto

# === CONFIGURAÇÃO ===
$model       = "tts_models/multilingual/multi-dataset/xtts_v2"
$image       = "ghcr.io/coqui-ai/tts:latest"
$cacheDir    = "E:\coqui tts cache"       # onde o cache de modelos é persistido
$outputDir   = "E:\tts_output"            # onde salvar os arquivos WAV
$language    = "pt"                        # sigla do idioma (pt para português)
$message     = "Eu te amo"                 # texto a ser sintetizado

# Lista de speakers (nomes) do modelo xtts_v2
$speakers = @(
    'Claribel Dervla','Daisy Studious','Gracie Wise','Tammie Ema','Alison Dietlinde','Ana Florence',
    'Annmarie Nele','Asya Anara','Brenda Stern','Gitta Nikolina','Henriette Usha','Sofia Hellen',
    'Tammy Grit','Tanja Adelina','Vjollca Johnnie','Andrew Chipper','Badr Odhiambo','Dionisio Schuyler',
    'Royston Min','Viktor Eka','Abrahan Mack','Adde Michal','Baldur Sanjin','Craig Gutsy','Damien Black',
    'Gilberto Mathias','Ilkin Urbano','Kazuhiko Atallah','Ludvig Milivoj','Suad Qasim','Torcull Diarmuid',
    'Viktor Menelaos','Zacharie Aimilios','Nova Hogarth','Maja Ruoho','Uta Obando','Lidiya Szekeres',
    'Chandra MacFarland','Szofi Granger','Camilla Holmström','Lilya Stainthorpe','Zofija Kendrick',
    'Narelle Moon','Barbora MacLean','Alexandra Hisakawa','Alma María','Rosemary Okafor','Ige Behringer',
    'Filip Traverse','Damjan Chapman','Wulf Carlevaro','Aaron Dreschner','Kumar Dahl','Eugenio Mataracı',
    'Ferran Simen','Xavier Hayasaka','Luis Moray','Marcos Rudaski'
)

# === PREPARA DIRETÓRIOS ===
if (!(Test-Path $cacheDir))  { New-Item -ItemType Directory $cacheDir | Out-Null }
if (!(Test-Path $outputDir)) { New-Item -ItemType Directory $outputDir | Out-Null }

# Sanitiza a mensagem para uso no nome de arquivo (substitui espaços e acentos)
$fileMsg = ($message -replace '[^\w]', '_')

Write-Host "Gerando áudio para mensagem: '$message' em idioma '$language' para cada speaker..."

# Itera sobre cada speaker e gera um arquivo WAV usando --speaker e --language
foreach ($speakerName in $speakers) {
    # Nome de arquivo seguro
    $fileSpeaker = ($speakerName -replace '[^\w]', '_')
    $outFile = "${fileMsg}_${language}_${fileSpeaker}.wav"

    Write-Host "-> $speakerName → $outFile"

    docker run --rm -it `
      --gpus all `
      -e TTS_HOME=/root/.cache/tts `
      -v "${cacheDir}:/root/.cache/tts" `
      -v "${outputDir}:/output" `
      $image `
        --model_name $model `
        --speaker_idx     "$speakerName" `
        --language_idx    $language `
        --text        "$message" `
        --out_path    "/output/$outFile"
}

Write-Host "Concluído! Arquivos salvos em $outputDir"
