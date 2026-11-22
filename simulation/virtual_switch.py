from .packet_queue import PacketQueue
from .qos_scheduler import QoSScheduler

class VirtualSwitch:
    def __init__(self, name, queue_capacity=256):
        self.name=name
        self.queues=[PacketQueue(queue_capacity) for _ in range(4)]
        self.scheduler=QoSScheduler(self.queues)
        self.flow_table=[]
    def install_rule(self, match, priority, output_port, queue_id):
        rule=next((r for r in self.flow_table if r['match']==match),None)
        if rule is None:
            rule={'match':match,'priority':priority,'output_port':output_port,'queue_id':queue_id,'active':True}
            self.flow_table.append(rule)
        else: rule.update(priority=priority,output_port=output_port,queue_id=queue_id,active=True)
        return rule
    def lookup_rule(self, packet):
        matches=[r for r in self.flow_table if r['active'] and all(getattr(packet,k,None)==v for k,v in r['match'].items())]
        return max(matches,key=lambda r:r['priority']) if matches else None
    def enqueue(self, packet, now, baseline=False):
        return self.queues[3 if baseline else packet.queue_id].push(packet, now)
