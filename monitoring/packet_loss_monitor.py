def loss_percent(generated, delivered): return 100*max(0,generated-delivered)/max(1,generated)
