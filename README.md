# SDN-Based QoS Management for Robotic Communication

A simulation-first SDN project that evaluates how QoS policies improve robotic communication performance under congestion, failover, and mixed-traffic conditions.

> **Important:** This repository is a **Python simulation**, not a real OpenFlow/Mininet/OVS deployment.

---

## 1) What this project does

This system compares two modes:

- **Baseline mode:** shared best-effort behavior
- **Proposed mode:** QoS-aware scheduling + congestion response + failover routing

It helps demonstrate how class-aware forwarding can reduce control-plane latency and improve reliability for critical robotic traffic.

---

## 2) Core features

- Centralized SDN controller logic for routing, QoS, and congestion handling
- Discrete-event network simulator with virtual hosts, links, queues, and switches
- Streamlit dashboard for live monitoring and interactive controls
- FastAPI backend for topology, status, metrics, events, and experiment APIs
- Built-in experiment suite with baseline vs proposed comparisons
- CSV/JSON/HTML export of results

---

## 3) QoS traffic classes

| Class | Traffic Type | DSCP | Queue | Priority |
|---|---|---:|---:|---|
| A | Critical Control | 46 | Q0 | Highest |
| B | Telemetry | 26 | Q1 | High |
| C | Video / Vision | 34 | Q2 | Medium |
| D | Bulk / Best Effort | 0 | Q3 | Lowest |

---

## 4) Architecture at a glance

### Layers

- **Application layer:** dashboard views and controls
- **Control layer:** controller managers (`controller/`)
- **Infrastructure layer:** packet-level simulation (`simulation/`)

### Topology behavior

- Normal path: `S1 -> S2 -> S3`
- Backup path on failure: `S1 -> S4 -> S3`

### Measurements

- latency
- jitter
- throughput
- delivery ratio
- packet loss

---

## 5) Repository structure

- `backend/` - FastAPI app and API routes
- `dashboard/` - Streamlit UI
- `controller/` - routing, QoS, congestion, topology, flow logic
- `simulation/` - network model and event simulation
- `traffic_generator/` - deterministic workload generators
- `monitoring/` - metric collection/analysis modules
- `experiments/` - scenario runners and exports
- `tests/` - pytest test suite
- `scripts/` - setup/start/stop/experiment PowerShell scripts
- `results/` - generated output artifacts
- `docs/` - architecture, algorithm, test and demo documentation

---

## 6) Prerequisites

- Windows 10/11
- Python **3.11**
- PowerShell

Dependencies are defined in `requirements.txt`.

---

## 7) Quick start (recommended)

Run from project root:

```powershell
.\scripts\setup_windows.ps1
.\scripts\start_project.ps1
```

Then open:

- **API Docs:** http://localhost:8000/docs
- **Dashboard:** http://localhost:8501

Stop services:

```powershell
.\scripts\stop_project.ps1
```

---

## 8) Manual start (optional)

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501
```

---

## 9) API overview

Base path: `/api`

- `GET /status` - controller + simulation status
- `GET /topology` - current topology details
- `GET /switches` - queue statistics per switch
- `GET /traffic-classes` - DSCP/class mapping
- `GET /qos` - active QoS state and policies
- `GET /metrics` - latest aggregated metrics
- `GET /events` - controller/simulator event logs
- `POST /simulation/start` - launch workload simulation
- `POST /congestion/start` - inject/test congestion state
- `POST /failover` - trigger route failover
- `POST /experiments/run` - execute all experiment scenarios

---

## 10) Dashboard highlights

- Topology and status monitoring
- QoS and congestion control toggles
- Failover trigger and event tracking
- Custom simulation configuration (duration/rates/sizes/mode)
- Performance analytics and downloadable results

---

## 11) Experiments

Run full experiment suite:

```powershell
.\scripts\run_experiments.ps1
```

Scenarios:

1. `S1_normal`
2. `S2_bulk_congestion`
3. `S3_video_streams`
4. `S4_primary_failure`
5. `S5_scalability`

For every scenario, both **baseline** and **proposed** modes are executed.

Generated outputs:

- `results/experiment_results.csv`
- `results/experiment_results.json`
- `results/*.html` (selected visualizations)

---

## 12) Testing and validation

```powershell
python -m pytest tests -v
python -m compileall .
```

---

## 13) Known limitations

- Simulation model is simplified for academic/case-study use
- Not a production SDN controller or real-time robotics safety system
- Traffic generation is deterministic periodic workload generation
- Dashboard and API maintain separate in-memory controller instances
- Results are simulated observations, not physical network benchmarks

---

## 14) Additional documentation

Refer to `docs/` for:

- architecture details
- algorithm notes
- implementation guide
- testing guide
- demo mode
- viva questions

---

## 15) License and usage

This repository is intended for educational and research demonstration purposes.
