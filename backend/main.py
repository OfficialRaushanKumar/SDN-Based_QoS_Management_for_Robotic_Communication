from fastapi import FastAPI
from .api import router
app=FastAPI(title='Robotic SDN QoS Simulation API',version='1.0.0')
app.include_router(router)
@app.get('/')
def root(): return {'name':'Robotic SDN QoS Simulation','docs':'/docs'}
