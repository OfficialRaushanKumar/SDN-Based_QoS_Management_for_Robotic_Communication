class TopologyManager:
    def __init__(self, simulator): self.simulator=simulator
    def validate(self): return all(n in self.simulator.graph for n in ('S1','S2','S4','S3','R1','H1'))
    def topology(self): return {'nodes':list(self.simulator.graph.nodes),'links':[{'source':a,'target':b,'capacity_mbps':d['link'].capacity_mbps,'utilization':d['link'].utilization,'available':d['link'].available} for a,b,d in self.simulator.graph.edges(data=True)]}
