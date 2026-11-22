from dataclasses import dataclass, field
from enum import Enum

class TrafficClass(str, Enum):
    CONTROL = "A"
    TELEMETRY = "B"
    VIDEO = "C"
    BULK = "D"

DSCP_CLASS = {46: TrafficClass.CONTROL, 26: TrafficClass.TELEMETRY, 34: TrafficClass.VIDEO, 0: TrafficClass.BULK}
CLASS_DSCP = {v: k for k, v in DSCP_CLASS.items()}
CLASS_QUEUE = {TrafficClass.CONTROL: 0, TrafficClass.TELEMETRY: 1, TrafficClass.VIDEO: 2, TrafficClass.BULK: 3}

@dataclass
class Packet:
    packet_id: str
    source: str
    destination: str
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int
    destination_port: int
    dscp: int
    traffic_class: TrafficClass
    queue_id: int
    size_bytes: int
    generation_time: float
    sequence_number: int
    path: list[str] = field(default_factory=list)
    hop_index: int = 0
    queue_entered: float = 0.0

    @classmethod
    def create(cls, packet_id, source, destination, dscp, size_bytes, generation_time, sequence_number=0):
        from .traffic_classifier import classify_dscp
        tc = classify_dscp(dscp)
        host_ips={'R1':'10.0.0.1','R2':'10.0.0.2','R3':'10.0.0.3','C1':'10.0.0.4','Bulk':'10.0.0.5','H1':'10.0.0.101','H2':'10.0.0.102','H3':'10.0.0.103'}
        return cls(str(packet_id), source, destination, host_ips.get(source,'10.0.0.250'),
                   host_ips.get(destination,'10.0.0.251'), "UDP" if tc.value in "AB" else "TCP",
                   20000, 30000, dscp, tc, CLASS_QUEUE[tc], size_bytes, generation_time, sequence_number)
