Add-Type -AssemblyName presentationCore
$duracao_total = 0
Get-ChildItem -Recurse -Filter *.wav | ForEach-Object {
    $m = New-Object System.Windows.Media.MediaPlayer
    $m.Open([uri]$_.FullName)
    Start-Sleep -Milliseconds 200
    $duracao_total += $m.NaturalDuration.TimeSpan.TotalSeconds
}
Write-Host ("Duração total: {0:N0} segundos" -f $duracao_total)
