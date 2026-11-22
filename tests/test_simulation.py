from simulation.network_simulator import NetworkSimulator
from traffic_generator import generate_workload
def test_forwards_packets():
    s=NetworkSimulator(); s.run(generate_workload(.1,1,['control']),.1); assert s.delivered and len(s.delivered)==len(s.generated)
def test_serialization_delay_matches_capacity():
    s=NetworkSimulator(); assert abs(s.link('S1','S2').serialization_seconds(1_000_000)-.08)<1e-9
def test_congestion_policing_records_packet_drops():
    s=NetworkSimulator(); s.run(generate_workload(.2,12,['bulk']),.2); assert any(reason=='qos_policing' for _,_,reason in s.drops)
