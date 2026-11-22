# SDN QoS Robotic Communication (Simulation)

A Python-based SDN case study that simulates QoS-aware traffic handling for robotic communication workloads.

> This project is a **network simulation** (not a hardware/OpenFlow deployment). It does not require Mininet, OVS, or physical switches.

## Overview

The system models three SDN layers:

- **Application layer**: Streamlit dashboard for monitoring, controls, and experiment analytics
- **Control layer**: centralized SDN controller and policy managers (`controller/`)
- **Infrastructure layer**: virtual hosts, links, switches, queues, and packet flow simulation (`simulation/`)

The simulator evaluates baseline vs QoS-aware behavior under normal load, congestion, video-heavy traffic, failover, and scale-up scenarios.

## QoS traffic classes

| Class | Type | DSCP | Queue |
|---|---|---:|---:|
| A | Critical Control | 46 | Q0 |
| B | Telemetry | 26 | Q1 |
| C | Video/Vision | 34 | Q2 |
| D | Best Effort/Bulk | 0 | Q3 |

## Architecture summary

- Topology includes hosts/robots connected through virtual switches (`S1`, `S2`, `S3`, `S4`)
- Normal path uses `S1 -> S2 -> S3`
- On primary-link failure, traffic is rerouted via `S1 -> S4 -> S3`
- Congestion and recovery use hysteresis-based state transitions
- Metrics include latency, jitter, packet delivery/loss, and throughput

## Project structure

- `backend/` - FastAPI service and API routes
- `dashboard/` - Streamlit web UI
- `controller/` - SDN logic (routing, QoS, congestion, flow/topology managers)
- `simulation/` - discrete-event packet/network simulator
- `traffic_generator/` - deterministic traffic workload generation
- `monitoring/` - metric collection and performance analysis
- `experiments/` - scenario runners and result export
- `tests/` - pytest unit tests
- `scripts/` - setup, start/stop, and experiment scripts (PowerShell)
- `results/` - generated CSV/JSON/HTML outputs

## Requirements

- Windows 10/11 (scripts provided for PowerShell)
- Python **3.11**

Core dependencies are listed in `requirements.txt` (FastAPI, Uvicorn, Streamlit, NetworkX, NumPy, Pandas, Plotly, Pytest).

## Quick start (Windows PowerShell)

From the project root:

```powershell
.\scripts\setup_windows.ps1
.\scripts\start_project.ps1
```

Open:

- API docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

To stop both services:

```powershell
.\scripts\stop_project.ps1
```

## Manual run (optional)

If you prefer manual commands:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501
```

## API highlights

Main endpoints (prefix: `/api`):

- `GET /status` - controller/simulation state and active path
- `GET /topology` - current simulated topology
- `GET /switches` - queue lengths, received, dropped
- `GET /traffic-classes` - class mapping and DSCP details
- `GET /qos` - QoS state and policies
- `GET /metrics` - latest measured metrics
- `GET /events` - controller and simulation events
- `POST /simulation/start` - run simulation workload
- `POST /congestion/start` - force/test congestion state
- `POST /failover` - trigger primary-link failover
- `POST /experiments/run` - run full experiment suite

## Dashboard usage

The dashboard provides:

- live status and topology views
- QoS and congestion controls
- failover action and event monitoring
- custom simulation form (duration, packet rates/sizes, baseline/proposed mode)
- experiment analytics and result charts

## Experiments

Run all scenarios:

```powershell
.\scripts\run_experiments.ps1
```

Scenarios include:

1. `S1_normal`
2. `S2_bulk_congestion`
3. `S3_video_streams`
4. `S4_primary_failure`
5. `S5_scalability`

Each scenario runs in both `baseline` and `proposed` modes and exports:

- `results/experiment_results.csv`
- `results/experiment_results.json`
- selected chart files in `results/*.html`

## Testing

```powershell
python -m pytest tests -v
python -m compileall .
```

## Important limitations

- This is a compact **discrete-event simulation**, not a real-time production controller
- Traffic generation is deterministic periodic workload generation
- QoS, admission, and control policies are intentionally simplified for case-study clarity
- Dashboard and API run as separate processes and keep separate in-memory controller instances
- Metrics are simulation outputs, not physical network measurements

## Documentation

See `docs/` for additional details:

- architecture
- algorithm notes
- demo mode
- implementation guide
- testing guide
- viva questions
