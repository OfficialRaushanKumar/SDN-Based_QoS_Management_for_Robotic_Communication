class RoutingManager:
    def __init__(self, simulator): self.simulator=simulator
    def path(self, source, destination): return self.simulator.shortest_path(source,destination)
    def fail_primary(self): self.simulator.set_link('S1','S2',False); return self.path('R1','H1')
    def restore_primary(self): self.simulator.set_link('S1','S2',True)
