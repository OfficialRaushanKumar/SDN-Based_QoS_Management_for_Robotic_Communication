from pathlib import Path
import pandas as pd
from controller.controller import SDNController
from traffic_generator import generate_workload
from monitoring.metrics_collector import collect_metrics
from time import perf_counter
ROOT=Path(__file__).resolve().parents[1]
def run_experiment(name,duration=3,scale=1,baseline=False,failure=False,video_scale=None):
    ctl=SDNController(baseline=baseline); sim=ctl.simulator
    failover_ms=0.0
    if failure:
        started=perf_counter(); ctl.routing.fail_primary(); ctl.routing.path('R1','H1'); failover_ms=(perf_counter()-started)*1000
    packets=generate_workload(duration,scale,selected=['control','telemetry','bulk'] if video_scale else None,seed=42)
    if video_scale: packets += generate_workload(duration,video_scale,selected=['video'],seed=42)
    offered=sum(p.size_bytes*8 for p in packets)/max(.001,duration)
    started=perf_counter(); ctl.detect_congestion(min(1.0,offered/(100_000_000))); reaction_ms=(perf_counter()-started)*1000
    sim.run(packets,duration)
    metrics=collect_metrics(sim)
    return {'scenario':name,'mode':'baseline' if baseline else 'proposed','controller_reaction_ms':reaction_ms,'failover_recovery_ms':failover_ms,**{f'{k}_{m}':v for k,d in metrics.items() for m,v in d.items()}},sim
def run_all(output_dir=None):
    out=Path(output_dir or ROOT/'results'); out.mkdir(parents=True,exist_ok=True); rows=[]
    for name,scale,failure,video_scale in [('S1_normal',1,False,None),('S2_bulk_congestion',12,False,None),('S3_video_streams',1,False,20),('S4_primary_failure',1,True,None),('S5_scalability',3,False,None)]:
        for baseline in (True,False): rows.append(run_experiment(name,3,scale,baseline,failure,video_scale)[0])
    df=pd.DataFrame(rows); df.to_csv(out/'experiment_results.csv',index=False); df.to_json(out/'experiment_results.json',orient='records',indent=2)
    import plotly.express as px
    for metric in ['A_latency_ms','A_loss_pct','C_throughput_mbps','D_throughput_mbps']:
        if metric in df: px.bar(df,x='scenario',y=metric,color='mode',barmode='group',title=f'Baseline vs proposed: {metric}',template='plotly_dark').write_html(out/f'{metric}.html',include_plotlyjs='cdn')
    return df
if __name__=='__main__': print(run_all().to_string(index=False))
