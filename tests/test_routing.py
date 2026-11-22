from simulation.network_simulator import NetworkSimulator
def test_backup_path_on_failure():
    s=NetworkSimulator(); s.set_link('S1','S2',False); assert 'S4' in s.shortest_path('R1','H1')
