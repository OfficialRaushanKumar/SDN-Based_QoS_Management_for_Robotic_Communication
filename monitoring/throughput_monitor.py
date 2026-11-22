def throughput_mbps(bytes_delivered, duration): return bytes_delivered*8/max(.001,duration)/1_000_000
