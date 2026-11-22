from simulation.network_simulator import NetworkSimulator
from .topology_manager import TopologyManager
from .flow_manager import FlowManager
from .qos_manager import QoSManager
from .congestion_detector import CongestionDetector
from .routing_manager import RoutingManager
from .event_logger import EventLogger
class SDNController:
    def __init__(self, **kwargs):
        self.simulator=NetworkSimulator(**kwargs); self.topology=TopologyManager(self.simulator)
        self.flows=FlowManager(); self.qos=QoSManager(); self.detector=CongestionDetector()
        self.routing=RoutingManager(self.simulator); self.logger=EventLogger(); self.running=False
        self.logger.log('controller_initialized','Windows software network simulation')
    def detect_congestion(self, utilization):
        state=self.detector.update(utilization)
        if state=='CONGESTED': self.qos.congested(); self.logger.log('congestion_detected',f'utilization={utilization:.3f}')
        elif state=='RECOVERY': self.qos.reset(); self.logger.log('congestion_cleared','normal policies restored')
        return state
