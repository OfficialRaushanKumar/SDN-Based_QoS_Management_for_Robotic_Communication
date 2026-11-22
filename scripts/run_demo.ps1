$ProjectRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $ProjectRoot '.venv\Scripts\python.exe') -c "from experiments.run_all_experiments import run_all; print(run_all().to_string(index=False))"
