from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from controller.controller import SDNController
from traffic_generator import generate_workload
from monitoring.metrics_collector import collect_metrics
router=APIRouter(prefix='/api'); controller=SDNController(); last_metrics={}
class StartRequest(BaseModel):
    duration:float=Field(5,gt=0,le=60)
    scale:float=Field(1,gt=0,le=10)
class CongestionRequest(BaseModel): utilization:float=Field(.95,ge=0,le=1)
@router.get('/status')
def status(): return {'controller':'running','simulation':'active' if controller.running else 'inactive','congestion':controller.qos.state,'active_path':'backup' if not controller.simulator.link('S1','S2').available else 'primary'}
@router.get('/topology')
def topology(): return controller.topology.topology()
@router.get('/switches')
def switches(): return [{'name':n,'queues':[{'id':i,'length':len(q.items),'received':q.received,'dropped':q.dropped} for i,q in enumerate(sw.queues)]} for n,sw in controller.simulator.switches.items()]
@router.get('/traffic-classes')
def classes(): return [{'class':'A','name':'Critical Control','dscp':46,'queue':0},{'class':'B','name':'Telemetry','dscp':26,'queue':1},{'class':'C','name':'Video/Vision','dscp':34,'queue':2},{'class':'D','name':'Best Effort/Bulk','dscp':0,'queue':3}]
@router.get('/qos')
def qos(): return {'state':controller.qos.state,'policies':controller.qos.policies}
@router.get('/metrics')
def metrics(): return last_metrics or collect_metrics(controller.simulator)
@router.get('/events')
def events(): return controller.logger.events+controller.simulator.events
@router.post('/simulation/start')
def start(req:StartRequest):
    global last_metrics
    try:
        controller.simulator=type(controller.simulator)(); controller.routing.simulator=controller.simulator; controller.topology.simulator=controller.simulator
        controller.running=True; packets=generate_workload(req.duration,req.scale); controller.simulator.run(packets,req.duration)
        last_metrics=collect_metrics(controller.simulator); controller.running=False; controller.logger.log('simulation_completed',f'{len(packets)} packets'); return {'ok':True,'metrics':last_metrics}
    except Exception as e:
        controller.running=False; raise HTTPException(400,str(e))
@router.post('/simulation/stop')
def stop(): controller.running=False; return {'ok':True}
@router.post('/congestion/start')
def congestion(req:CongestionRequest): return {'state':controller.detect_congestion(req.utilization),'policies':controller.qos.policies}
@router.post('/congestion/stop')
def congestion_stop(): controller.detect_congestion(0); return {'state':controller.qos.state}
@router.post('/failover')
def failover():
    path=controller.routing.fail_primary(); controller.logger.log('backup_route_activated',str(path)); return {'path':path,'active':bool(path)}
@router.post('/qos/reset')
def qos_reset(): controller.qos.reset(); controller.routing.restore_primary(); return {'state':controller.qos.state}
@router.post('/experiments/run')
def experiments():
    from experiments.run_all_experiments import run_all
    return {'rows':run_all().to_dict(orient='records')}
