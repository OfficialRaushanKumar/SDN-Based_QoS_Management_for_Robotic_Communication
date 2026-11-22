import networkx as nx
from .packet import Packet, TrafficClass
from .virtual_link import VirtualLink
from .virtual_switch import VirtualSwitch

class NetworkSimulator:
    """Deterministic, time-stepped store-and-forward packet simulator."""
    def __init__(self, seed=42, queue_capacity=256, primary_capacity=100, backup_capacity=80, baseline=False):
        self.seed=seed; self.queue_capacity=queue_capacity; self.baseline=baseline; self.time=0.0
        self.graph=nx.Graph(); self.switches={n:VirtualSwitch(n,queue_capacity) for n in ('S1','S2','S4','S3')}
        self.links={}; self.generated=[]; self.delivered=[]; self.drops=[]; self.events=[]; self.active_path='primary'
        self.metrics=[]; self._setup(primary_capacity,backup_capacity)
        self.adaptive_qos=not baseline
    def _edge(self,a,b,cap):
        link=VirtualLink(a,b,cap); self.links[tuple(sorted((a,b)))]=link; self.graph.add_edge(a,b,link=link,weight=1)
    def _setup(self,p,b):
        for n in ['R1','R2','R3','C1','Bulk','H1','H2','H3']: self.graph.add_node(n)
        self._edge('S1','S2',p); self._edge('S2','S3',p); self._edge('S1','S4',b); self._edge('S4','S3',b)
        for h in ['R1','R2','R3','C1','Bulk']: self._edge(h,'S1',1000)
        for h in ['H1','H2','H3']: self._edge(h,'S3',1000)
    def link(self,a,b): return self.links[tuple(sorted((a,b)))]
    def set_link(self,a,b,available):
        self.link(a,b).available=available; self.events.append({'time':self.time,'event':'link_up' if available else 'link_down','detail':f'{a}-{b}'})
    def shortest_path(self,src,dst):
        g=self.graph.copy()
        for a,b,d in list(g.edges(data=True)):
            if not d['link'].available: g.remove_edge(a,b)
        try: return nx.shortest_path(g,src,dst)
        except nx.NetworkXNoPath: return []
    def send(self, packet):
        self.generated.append(packet)
        packet.path=self.shortest_path(packet.source,packet.destination)
        if not packet.path: self.drops.append((packet,self.time,'no_route')); return
        for index,switch in enumerate(packet.path[1:-1],start=1):
            if switch in self.switches:
                self.switches[switch].install_rule({'source':packet.source,'destination':packet.destination,'dscp':packet.dscp},
                    100-packet.queue_id,packet.path[index+1],3 if self.baseline else packet.queue_id)
        packet.hop_index=0
        self._forward(packet,self.time)
    def _forward(self,p,now):
        if p.hop_index >= len(p.path)-1:
            self.delivered.append((p,now)); return
        a,b=p.path[p.hop_index:p.hop_index+2]; link=self.link(a,b)
        if not link.available: self.drops.append((p,now,'link_down')); return
        if a in self.switches:
            sw=self.switches[a]
            rule=sw.lookup_rule(p)
            if rule:
                p.queue_id=rule['queue_id']
                b=rule['output_port']
                link=self.link(a,b)
            if not sw.enqueue(p,now,self.baseline): self.drops.append((p,now,'queue_overflow')); return
            p=sw.scheduler.next_packet(now)
            if p is None: return
        tx=link.serialization_seconds(p.size_bytes); start=max(now,link.busy_until); finish=start+tx
        link.busy_until=finish; link.bytes_sent+=p.size_bytes; link.packets_sent+=1
        p.hop_index+=1
        # Simulator advances all scheduled packet events in a deterministic local event list.
        import heapq
        heapq.heappush(self._events,(finish+link.propagation_ms/1000,next(self._event_seq),p))
    def run(self, packets, duration=10.0, step=0.001):
        import heapq
        import itertools
        self._events=[]; arrivals=sorted(packets,key=lambda x:x.generation_time); ai=0; t=0.0
        self._event_seq=itertools.count()
        offered=sum(p.size_bytes*8 for p in arrivals)/max(.001,duration)
        congested=offered >= .8*self.link('S1','S2').capacity_mbps*1_000_000
        policer={'C':(30_000_000,0.0,0.0),'D':(5_000_000,0.0,0.0)}
        while ai<len(arrivals) or self._events:
            next_arrival=arrivals[ai].generation_time if ai<len(arrivals) else float('inf')
            next_event=self._events[0][0] if self._events else float('inf')
            t=min(next_arrival,next_event)
            if t>duration and ai<len(arrivals): break
            self.time=t
            while ai<len(arrivals) and arrivals[ai].generation_time<=t+1e-12 and t<=duration:
                packet=arrivals[ai]; ai+=1
                cls=packet.traffic_class.value
                if self.adaptive_qos and congested and cls in policer:
                    limit,tokens,last=policer[cls]
                    tokens=min(limit,tokens+max(0,t-last)*limit)
                    need=packet.size_bytes*8
                    if tokens < need:
                        self.generated.append(packet); self.drops.append((packet,t,'qos_policing')); policer[cls]=(limit,tokens,t); continue
                    policer[cls]=(limit,tokens-need,t)
                self.send(packet)
            while self._events and self._events[0][0]<=t+1e-12:
                at,_,p=heapq.heappop(self._events); self.time=at; self._forward(p,at)
        self.time=duration
        for link in self.links.values(): link.measurement_window=max(.001,duration)
        return self
