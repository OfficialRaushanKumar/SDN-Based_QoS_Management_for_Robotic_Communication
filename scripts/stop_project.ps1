$ProjectPorts = @(8000, 8501)
$ListenerIds = @()
foreach ($Line in (netstat -ano -p tcp | Select-String 'LISTENING')) {
  $Fields = $Line.Line.Trim() -split '\s+'
  if ($Fields.Count -ge 5) {
    $LocalPort = 0
    if ([int]::TryParse(($Fields[1] -split ':')[-1], [ref]$LocalPort) -and $ProjectPorts -contains $LocalPort) {
      $ListenerIds += [int]$Fields[4]
    }
  }
}
$ListenerIds | Sort-Object -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Write-Host 'Project listeners on ports 8000 and 8501 stopped.'
