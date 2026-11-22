from controller.congestion_detector import CongestionDetector
def test_hysteresis():
    d=CongestionDetector(.8,.6); assert d.update(.85)=='CONGESTED'; assert d.update(.7)=='CONGESTED'; assert d.update(.5)=='RECOVERY'
