$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { throw 'Run .\scripts\setup_windows.ps1 first.' }
Start-Process -FilePath $Python -ArgumentList '-m uvicorn backend.main:app --host 127.0.0.1 --port 8000' -WorkingDirectory $ProjectRoot -WindowStyle Hidden
Start-Process -FilePath $Python -ArgumentList '-m streamlit run dashboard/app.py --server.port 8501' -WorkingDirectory $ProjectRoot -WindowStyle Hidden
Write-Host 'API: http://localhost:8000/docs'; Write-Host 'Dashboard: http://localhost:8501'
