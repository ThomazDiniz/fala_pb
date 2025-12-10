# Cria pasta converted no diretório atual
$converted = Join-Path (Get-Location) "converted"
if (!(Test-Path $converted)) {
    New-Item -ItemType Directory -Path $converted | Out-Null
}

# Percorre todos os WAVs do diretório atual
Get-ChildItem -File -Filter *.wav | ForEach-Object {
    $input = $_.FullName
    $output = Join-Path $converted $_.Name

    ffmpeg -y -i "$input" -ac 1 -ar 22050 -sample_fmt s16 "$output"

    Write-Host "Convertido: $($_.Name)"
}

Write-Host "Conversão concluída. Arquivos em: $converted"
