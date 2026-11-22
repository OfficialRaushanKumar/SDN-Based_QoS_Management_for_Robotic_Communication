from simulation.packet import Packet
TRAFFIC={'control':(46,'R1','H1',96,40),'telemetry':(26,'R2','H1',160,80),'video':(34,'C1','H2',1200,500),'bulk':(0,'Bulk','H3',1400,1200)}
def generate_workload(duration=10.0, scale=1.0, selected=None, seed=42):
    selected=selected or list(TRAFFIC); out=[]
    for name in selected:
        dscp,src,dst,size,rate=TRAFFIC[name]; n=max(0,int(rate*scale*duration))
        for i in range(n): out.append(Packet.create(f'{name}-{i}',src,dst,dscp,size,i/(rate*scale),i))
    return sorted(out,key=lambda p:p.generation_time)

def generate_custom_workload(duration, rates_pps, sizes_bytes):
    """Build a user-configured, deterministic workload for the dashboard form."""
    specs={
        'control':(46,'R1','H1'),
        'telemetry':(26,'R2','H1'),
        'video':(34,'C1','H2'),
        'bulk':(0,'Bulk','H3'),
    }
    packets=[]
    for name,(dscp,source,destination) in specs.items():
        rate=max(0.0,float(rates_pps.get(name,0)))
        size=max(64,int(sizes_bytes.get(name,64)))
        count=int(rate*duration)
        for seq in range(count):
            packets.append(Packet.create(f'custom-{name}-{seq}',source,destination,dscp,size,seq/rate,seq))
    return sorted(packets,key=lambda packet:packet.generation_time)
