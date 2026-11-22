def jitter_ms(delays): return sum(abs(b-a) for a,b in zip(delays,delays[1:]))*1000/max(1,len(delays)-1)
