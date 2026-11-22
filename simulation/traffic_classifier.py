from .packet import DSCP_CLASS
def classify_dscp(dscp):
    try: return DSCP_CLASS[int(dscp)]
    except (KeyError,ValueError,TypeError): return DSCP_CLASS[0]
