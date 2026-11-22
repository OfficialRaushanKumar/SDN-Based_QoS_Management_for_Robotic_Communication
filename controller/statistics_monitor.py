class StatisticsMonitor:
    def __init__(self): self.samples=[]
    def record(self, sample): self.samples.append(sample)
