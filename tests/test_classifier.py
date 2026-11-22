from simulation.traffic_classifier import classify_dscp
from simulation.packet import TrafficClass
def test_dscp_classes():
    assert classify_dscp(46)==TrafficClass.CONTROL
    assert classify_dscp(26)==TrafficClass.TELEMETRY
    assert classify_dscp(34)==TrafficClass.VIDEO
    assert classify_dscp(0)==TrafficClass.BULK
