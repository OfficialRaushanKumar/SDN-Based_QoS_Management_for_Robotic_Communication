from collections import deque

class PacketQueue:
    def __init__(self, capacity=256):
        self.capacity = capacity
        self.items = deque()
        self.received = self.transmitted = self.dropped = 0
        self.wait_samples = []
        self.length_samples = []
    def push(self, packet, now):
        self.received += 1
        if len(self.items) >= self.capacity:
            self.dropped += 1
            return False
        packet.queue_entered = now
        self.items.append(packet)
        self.length_samples.append(len(self.items))
        return True
    def pop(self, now):
        if not self.items: return None
        p = self.items.popleft(); self.transmitted += 1
        self.wait_samples.append(max(0.0, now-p.queue_entered))
        return p
    @property
    def average_length(self): return sum(self.length_samples)/len(self.length_samples) if self.length_samples else 0.0
    @property
    def average_wait(self): return sum(self.wait_samples)/len(self.wait_samples) if self.wait_samples else 0.0
