$ProjectRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $ProjectRoot '.venv\Scripts\python.exe') -m streamlit run (Join-Path $ProjectRoot 'dashboard\app.py') --server.port 8501
