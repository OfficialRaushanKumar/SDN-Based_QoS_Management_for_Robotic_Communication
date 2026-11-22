class QoSManager:
    def __init__(self): self.state='NORMAL'; self.policies={'A':'protected','B':'high','C':'normal','D':'normal'}
    def congested(self):
        self.state='CONGESTED'; self.policies={'A':'protected','B':'prioritized','C':'rate_controlled','D':'rate_limited'}
    def reset(self): self.state='NORMAL'; self.policies={'A':'protected','B':'high','C':'normal','D':'normal'}
