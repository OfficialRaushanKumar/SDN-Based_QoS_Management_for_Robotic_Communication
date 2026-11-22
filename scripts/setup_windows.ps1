$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Launcher = Get-Command py -ErrorAction SilentlyContinue
if ($Launcher) {
  & $Launcher.Source -3.11 --version
  if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 was not found. Install Python 3.11 and enable the py launcher.' }
  $PythonCommand = $Launcher.Source
  $PythonArgs = @('-3.11')
} else {
  $Python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $Python) { throw 'Python 3.11 was not found. Install Python 3.11 and enable the py launcher.' }
  $VersionText = (& $Python.Source --version 2>&1 | Out-String).Trim()
  if ($VersionText -notmatch '^Python 3\.11\.') { throw "Python 3.11 is required; found $VersionText." }
  $PythonCommand = $Python.Source
  $PythonArgs = @()
}
Push-Location $ProjectRoot
try {
  & $PythonCommand @PythonArgs -m venv .venv
  if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
  & .\.venv\Scripts\python.exe -m pip install --upgrade pip
  & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
  New-Item -ItemType Directory -Force results | Out-Null
  & .\.venv\Scripts\python.exe -c "import fastapi,uvicorn,streamlit,networkx,numpy,pandas,plotly"
  if ($LASTEXITCODE -ne 0) { throw 'Dependency validation failed.' }
  Write-Host 'Setup complete. Use .\scripts\start_project.ps1'
} finally { Pop-Location }
