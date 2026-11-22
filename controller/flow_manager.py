class FlowManager:
    def __init__(self): self.rules=[]
    def install(self,match,priority,output_port,queue_id):
        rule={'match':match,'priority':priority,'output_port':output_port,'queue_id':queue_id,'active':True}; self.rules.append(rule); return rule
