from fastapi import FastAPI

from infrastructure.quotehistory_collection import quotehistoryCollection
from api.fxopen_api import FxOpenApi
from dateutil import parser

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/quotehistory-collection")
def get_quotehistory_collection():
    quotehistoryCollection.LoadQuotehistoryDB()
    return quotehistoryCollection.quotehistory_dict


@app.get("/api/account")
def get_account():
    api = FxOpenApi()
    return api.get_account()


@app.get("/api/quotehistory")
def get_quotehistory():
    api = FxOpenApi()
    return api.get_quotehistory()


@app.get("/api/prices-candle/{pair}/{granularity}/{date_f}")
def get_quotehistory(pair: str, granularity: str, date_f: str):
    api = FxOpenApi()
    dfr = parser.parse(date_f)
    # dfr = parser.parse("2024-08-12T04:00:00Z")
    df_candles = api.get_candles_df(pair=pair, count=-10, granularity=granularity, date_f=dfr)

    return df_candles.to_dict("list")


@app.get("/api/last-complete-candle/{pair}/{granularity}")
def last_complete_candle(pair: str, granularity: str):
    api = FxOpenApi()
    df_candle = api.last_complete_candle(pair=pair, granularity=granularity)

    return df_candle
