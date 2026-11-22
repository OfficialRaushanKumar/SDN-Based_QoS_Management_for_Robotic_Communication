# Adaptive rule based closed loop QoS

Configured congestion and recovery thresholds are 0.80 and 0.60 utilization. Hysteresis leaves the state unchanged between thresholds.

```text
sample link utilization
if NORMAL and utilization >= 0.80:
    protect A, prioritize B, rate control C, limit D
    evaluate alternate route availability and capacity
if CONGESTED and utilization <= 0.60:
    restore default class policy and primary route when available
log every state transition
```

This is an adaptive rule based closed loop management design, not a newly invented algorithm. Path selection removes unavailable links and computes a NetworkX shortest path. Serialization delay is packet bits / link bits per second; propagation delay is added per traversed link. No artificial loss or latency is inserted.
