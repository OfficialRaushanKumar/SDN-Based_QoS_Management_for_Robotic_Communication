# Implementation guide

`simulation/packet.py` defines packet fields and DSCP mappings. `network_simulator.py` owns the graph, links, virtual switches and event clock. Each packet advances hop by hop and link busy time enforces serialization. `controller/controller.py` composes topology, flow, QoS, congestion and routing managers. `traffic_generator/traffic_manager.py` creates deterministic periodic packet workloads. `monitoring/metrics_collector.py` calculates per class delay, jitter, delivery, loss and throughput from simulator records.

`backend/main.py` exposes the API router. `dashboard/app.py` renders the monitoring and control pages. `experiments/run_all_experiments.py` runs five workload scenarios in both baseline and proposed mode and exports CSV and JSON. PowerShell setup and launch scripts are in `scripts/`.
