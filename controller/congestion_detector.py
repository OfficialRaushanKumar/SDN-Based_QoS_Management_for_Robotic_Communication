class CongestionDetector:
    def __init__(self, threshold=.8, recovery=.6): self.threshold=threshold; self.recovery=recovery; self.congested=False
    def update(self, utilization):
        if not self.congested and utilization>=self.threshold: self.congested=True; return 'CONGESTED'
        if self.congested and utilization<=self.recovery: self.congested=False; return 'RECOVERY'
        return 'NORMAL' if not self.congested else 'CONGESTED'
