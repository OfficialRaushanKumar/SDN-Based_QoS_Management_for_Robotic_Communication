from simulation.network_simulator import NetworkSimulator
from traffic_generator import generate_workload
from monitoring.metrics_collector import collect_metrics
def test_metrics_are_measured():
    s=NetworkSimulator(); s.run(generate_workload(.1,1,['control']),.1); m=collect_metrics(s); assert m['A']['delivered']>0 and m['A']['latency_ms']>=0
