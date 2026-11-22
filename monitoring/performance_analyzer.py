from .metrics_collector import collect_metrics
def compare(baseline, proposed): return {'baseline':collect_metrics(baseline),'proposed':collect_metrics(proposed)}
