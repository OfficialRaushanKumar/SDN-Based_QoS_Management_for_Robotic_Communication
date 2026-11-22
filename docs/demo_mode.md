# Demonstration run sheet (8–12 minutes)

Use the Dashboard sidebar's **Run Demo Mode** control to execute fresh S1–S5 workloads in baseline and proposed modes. It computes results from the simulator and saves them; it does not play back stored sample metrics.

1. Launch the app and explain that all switches/links are software models (1 minute).
2. Show the network topology and primary/backup routes (1 minute).
3. Show DSCP 46/26/34/0 and queues Q0–Q3 (1 minute).
4. Start normal traffic on Overview and inspect generated/delivered class metrics (1 minute).
5. Trigger 95% congestion on Congestion Management and show policy state; the S2/S3 workloads also cross the bottleneck to demonstrate policing (2 minutes).
6. Open Performance Analytics and compare fresh baseline/proposed metrics and saved CSV results (2 minutes).
7. Fail S1–S2 on the Failover page and show path through S4, then restore the primary (1 minute).
8. Clear congestion and finish with event records and analytics (1–2 minutes).

Timing includes narration and page changes. Simulator runs complete faster than the presentation duration.
