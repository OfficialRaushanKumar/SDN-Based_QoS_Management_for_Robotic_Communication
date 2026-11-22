from simulation.traffic_classifier import classify_dscp
from simulation.packet import CLASS_QUEUE
def classify(packet):
    packet.traffic_class=classify_dscp(packet.dscp); packet.queue_id=CLASS_QUEUE[packet.traffic_class]
    return packet.traffic_class
