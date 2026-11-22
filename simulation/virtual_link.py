from dataclasses import dataclass

@dataclass
class VirtualLink:
    source: str
    target: str
    capacity_mbps: float
    propagation_ms: float = 1.0
    available: bool = True
    bytes_sent: int = 0
    packets_sent: int = 0
    packets_dropped: int = 0
    busy_until: float = 0.0
    measurement_window: float = 1.0
    def serialization_seconds(self, size_bytes): return size_bytes*8/(self.capacity_mbps*1_000_000)
    @property
    def utilization(self): return min(1.0, self.bytes_sent*8/(max(.001,self.measurement_window)*self.capacity_mbps*1_000_000))
