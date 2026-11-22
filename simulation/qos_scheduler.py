class QoSScheduler:
    """Strict priority for A; weighted round-robin service for B/C/D."""
    def __init__(self, queues, weights=(5, 3, 1)):
        self.queues = queues
        self.weights = weights
        self.cycle = [1]*weights[0] + [2]*weights[1] + [3]*weights[2]
        self.cursor = 0
    def next_packet(self, now):
        if self.queues[0].items: return self.queues[0].pop(now)
        for _ in range(len(self.cycle)):
            q = self.cycle[self.cursor]; self.cursor = (self.cursor+1) % len(self.cycle)
            if self.queues[q].items: return self.queues[q].pop(now)
        return None
