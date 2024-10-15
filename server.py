from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import http
import pandas as pd
import datetime as dt

from strategies import donchian_trend
from technicals.indicators import Donchian
from infrastructure.quotehistory_collection import quotehistoryCollection
from api.fxopen_api import FxOpenApi
from api.web_options import get_options
from dateutil import parser

from db.db import DataDB

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def add_timestr(df):
    df['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") 
                    for x in df['time']]
    return df
        
def get_response(data):
    if data is None:
        return dict(message="error getting data"), http.HTTPStatus.NOT_FOUND
    else:
        return data


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/quotehistory-collection")
def get_quotehistory_collection():
    quotehistoryCollection.LoadQuotehistoryDBFiltered()
    return get_response(quotehistoryCollection.quotehistory_dict)


@app.get("/api/account")
def get_account():
    api = FxOpenApi()
    return get_response(api.get_account())


@app.get("/api/options")
def get_account():
    return get_response(get_options())


@app.get("/api/quotehistory")
def get_quotehistory():
    api = FxOpenApi()
    return get_response(api.get_quotehistory())


@app.get("/api/prices-candle-db/{pair}/{granularity}/{count}")
def get_prices_candle_db(pair: str, granularity: str, count:int):
    db = DataDB()
    data = db.query_all_list(f'{pair}_{granularity}', count)
    data = add_timestr(data)
    return get_response(data)

@app.get("/api/prices-candle/{pair}/{granularity}/{count}")
def get_prices_candle(pair: str, granularity: str, count:int):
    api = FxOpenApi()
    df = api.get_candles_df(
        pair=pair, count=count*-1, granularity=granularity
    )
    df = add_timestr(df)
    return get_response(df.to_dict("list"))

@app.get("/api/prices-candle/{pair}/{granularity}/{date_f}")
def get_prices_candle(pair: str, granularity: str, date_f: str):
    api = FxOpenApi()
    dfr = parser.parse(date_f)
    # dfr = parser.parse("2024-08-12T04:00:00Z")
    df = api.get_candles_df(
        pair=pair, count=-10, granularity=granularity, date_f=dfr
    )
    df = add_timestr(df)
    return get_response(df.to_dict("list"))

@app.get("/api/last-complete-candle/{pair}/{granularity}")
def last_complete_candle(pair: str, granularity: str):
    api = FxOpenApi()
    df_candle = api.last_complete_candle(pair=pair, granularity=granularity)

    return get_response(df_candle)


@app.get("/api/technicals/indicator/donchian/{pair}/{granularity}/{count}/{window}")
def indicator_donchian(pair: str, granularity: str, count:int, window: int):
    db = DataDB()
    df = db.query_all(f'{pair}_{granularity}', count)
    df = pd.DataFrame(df)

    df = Donchian(df, window)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    df = add_timestr(df)
    
    return get_response(df.to_dict("list"))


@app.get("/api/single-backtest/{pair}/{granularity}/{window}/{prewindow}/{strategy}")
def single_backtest(pair: str, granularity: str, window: int, prewindow: int, strategy: str):
    db = DataDB()
    df = db.query_all(f'{pair}_{granularity}', None)
    df = pd.DataFrame(df)

    result = {}

    if strategy == 'donchian-trend':
        df = Donchian(df, window)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        result = donchian_trend.run_strategy()

    return get_response(result)
