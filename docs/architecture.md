# Architecture

## Logical SDN layers

Application: dashboard views for classification, QoS, congestion, failover and performance. Control: Python controller owns topology, simulated flow rules, congestion state, QoS policy, path selection and event records. Infrastructure: virtual robots, bulk host, servers, switches, bounded packet queues and capacity constrained links.

## Topology and packet path

R1, R2, R3, C1 and Bulk connect to S1. S1 connects to S2 and S4; both connect to S3. H1, H2 and H3 attach to S3. Normal routing uses S1-S2-S3. If S1-S2 is unavailable, shortest path on the remaining graph traverses S1-S4-S3. Packet generation creates DSCP tagged packets, the classifier maps DSCP to one of four queues, and the simulation advances packet events through links with serialization and propagation delay.

The API and Streamlit are separate processes and currently hold separate in-memory controller instances. Results persist in CSV/JSON files.
