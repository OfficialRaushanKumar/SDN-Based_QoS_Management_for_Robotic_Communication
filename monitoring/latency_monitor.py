def latency_ms(packet, delivered_at): return max(0.0,(delivered_at-packet.generation_time)*1000)
