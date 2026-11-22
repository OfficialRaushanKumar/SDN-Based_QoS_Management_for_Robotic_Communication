# Testing and experiment guide

From the project directory run `python -m pytest tests -v`, then `python -m compileall .`. Start the API with `python -m uvicorn backend.main:app --port 8000` and open `/docs`; start the dashboard with `python -m streamlit run dashboard/app.py --server.port 8501`.

Use the Performance Analytics page or `.\scripts\run_experiments.ps1` to generate S1 normal, S2 high offered load, S3 video stream load, S4 primary link failure, and S5 increased offered flows. Compare the paired `baseline` and `proposed` rows in `results/experiment_results.csv`. Counts and delay values are simulator observations.
