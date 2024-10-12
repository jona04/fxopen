import constants.defs as defs
from infrastructure.quotehistory_collection import quotehistoryCollection as qc
from api.fxopen_api import FxOpenApi

def make_option(k):
    return dict(key=k, label=k, value=k)


def get_options():
    qc.LoadQuotehistoryDB()
    
    ps = [p for p in qc.quotehistory_dict.keys()]
    ps.sort()

    return dict(
        granularities=[make_option(g) for g in defs.TFS.keys()],
        pairs=[make_option(p) for p in ps]
    )