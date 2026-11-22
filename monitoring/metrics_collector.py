from collections import defaultdict
def collect_metrics(sim):
    groups=defaultdict(list)
    for p,t in sim.delivered: groups[p.traffic_class.value].append((p.sequence_number,max(0,t-p.generation_time)))
    out={}
    for cls in ['A','B','C','D']:
        records=sorted(groups[cls]); delays=[d for _,d in records]; generated=[p for p in sim.generated if p.traffic_class.value==cls]
        got=sum(1 for p,t in sim.delivered if p.traffic_class.value==cls); loss=max(0,len(generated)-got)
        sd=sorted(delays); jitter=sum(abs(b-a) for a,b in zip(sd,sd[1:]))/max(1,len(sd)-1)
        bits=sum(p.size_bytes*8 for p,t in sim.delivered if p.traffic_class.value==cls)
        out[cls]={'generated':len(generated),'delivered':got,'dropped':loss,'latency_ms':sum(delays)/len(delays)*1000 if delays else 0,'jitter_ms':jitter*1000,'loss_pct':100*loss/max(1,len(generated)),'throughput_mbps':bits/max(.001,sim.time)/1e6}
    out['overall']={'generated':len(sim.generated),'delivered':len(sim.delivered),'dropped':sum(out[k]['dropped'] for k in 'ABCD'),'throughput_mbps':sum(out[k]['throughput_mbps'] for k in 'ABCD')}
    return out
