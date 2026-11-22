from .traffic_manager import generate_workload
def generate(duration=10, rate_scale=1): return generate_workload(duration,rate_scale,['control'])
