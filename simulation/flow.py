from dataclasses import dataclass

@dataclass
class Flow:
    flow_id: str
    source: str
    destination: str
    dscp: int
    packet_rate_pps: float
    packet_size_bytes: int
    enabled: bool = True
