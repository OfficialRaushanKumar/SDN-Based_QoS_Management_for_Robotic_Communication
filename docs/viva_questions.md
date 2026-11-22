# Viva questions and answers

1. **What is SDN?** A network design that separates centralized control decisions from packet forwarding.
2. **What does the controller do here?** Maintains simulated topology, class policy, route and event state.
3. **Is this physical OpenFlow?** No; switches and forwarding are Python models.
4. **Why centralize control?** It gives one place to observe policy and select routes.
5. **What are the three layers?** Application, control and infrastructure.
6. **What is QoS?** Differentiated treatment for traffic with different service needs.
7. **What is DSCP?** The IP header differentiated services code point used here as a class marker.
8. **What are the four classes?** Control A, telemetry B, video C and bulk D.
9. **What DSCP is control?** 46.
10. **What DSCP is telemetry?** 26.
11. **What DSCP is video?** 34.
12. **What DSCP is bulk?** 0.
13. **What are Q0-Q3?** The bounded class queues at modeled switches.
14. **What is strict priority?** Serving the critical queue before lower classes.
15. **How is starvation reduced?** Lower queues receive weighted round robin opportunities.
16. **What causes congestion state?** Measured utilization crossing the configured threshold.
17. **Why hysteresis?** To avoid rapid state switching around one boundary.
18. **What is recovery threshold?** The lower utilization boundary used to clear congestion state.
19. **How is serialization delay computed?** Packet bits divided by link bit rate.
20. **What contributes to latency?** Link serialization and propagation plus model queue waiting.
21. **What is jitter?** Variation in measured packet delay.
22. **How is loss calculated?** Generated packet count minus delivered packet count.
23. **How is throughput calculated?** Delivered bits divided by simulated duration.
24. **What is the primary route?** S1-S2-S3 between access and server switches.
25. **What is the backup route?** S1-S4-S3.
26. **How does failover occur?** A failed edge is removed from path calculation.
27. **Why NetworkX?** It provides graph storage and shortest path routines.
28. **What is a virtual switch?** A software object with queues and a scheduler.
29. **What is a virtual link?** A capacity and propagation model with availability and busy time.
30. **What is baseline mode?** All packets share the best effort queue.
31. **What is proposed mode?** DSCP classes, class queues and controller policies.
32. **How are workloads repeatable?** They use deterministic periodic generation times.
33. **What does FastAPI provide?** JSON endpoints for topology, state, metrics and controls.
34. **What does Streamlit provide?** Interactive monitoring, charts and simulation controls.
35. **What are model limitations?** It is not a physical network and simplifies policing and queue service.
36. **Can this prove robot safety?** No; safety needs real time validation and deployment testing.
37. **What does CSV export contain?** Per-scenario and mode metric rows from each run.
