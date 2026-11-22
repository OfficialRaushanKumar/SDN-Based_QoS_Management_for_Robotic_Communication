$ProjectRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $ProjectRoot '.venv\Scripts\python.exe') -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
