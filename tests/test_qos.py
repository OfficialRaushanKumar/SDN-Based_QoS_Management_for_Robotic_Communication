from simulation.packet_queue import PacketQueue
from simulation.qos_scheduler import QoSScheduler
from simulation.packet import Packet
def test_scheduler_prefers_critical():
    queues=[PacketQueue(4) for _ in range(4)]
    a=Packet.create('a','R1','H1',46,64,0); d=Packet.create('d','Bulk','H3',0,64,0)
    queues[3].push(d,0); queues[0].push(a,0)
    assert QoSScheduler(queues).next_packet(0)==a
def test_queue_is_bounded():
    q=PacketQueue(1); p=Packet.create('a','R1','H1',46,64,0)
    assert q.push(p,0) and not q.push(p,0) and q.dropped==1
