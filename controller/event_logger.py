from datetime import datetime, timezone
class EventLogger:
    def __init__(self): self.events=[]
    def log(self,event,detail=''):
        self.events.append({'timestamp':datetime.now(timezone.utc).isoformat(),'event':event,'detail':detail})
