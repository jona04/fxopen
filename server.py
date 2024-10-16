from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import http
import pandas as pd
import datetime as dt

from simulation.donchian_trend import DonchianTrend
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


@app.get("/api/single-backtest/{pair}/{granularity}/{window}/{prewindow}/{ema_window}/{strategy}")
def single_backtest(pair: str, granularity: str, window: int, ema_window:int, prewindow: int, strategy: str):
    db = DataDB()
    df = db.query_all(f'{pair}_{granularity}', None)
    df = pd.DataFrame(df)

    result = {}

    if strategy == 'donchian-trend':

        # def run_pair(pair,pip_value,granularity='M5',use_spread=True,
        #      stop_loss = 1000, take_profit = 200, 
        #      fixed_tp_sl=True,trans_cost=8,
        #      neg_multiplier=1.5, rev=True,
        #     spread_limit=50,ema_1 = 10,donchian_window = 10000, donchian_window_prev = 100):

        df = Donchian(df, window)
        df[f'EMA_short'] = df.mid_c.ewm(span=ema_window, min_periods=ema_window).mean()
        df['SPREAD'] = (df[f'ask_c'] - df[f'bid_c']) / pip_value
        df['donchian_size'] = (df['donchian_high'] - df['donchian_low'])/pip_value
        df['TP'] = 0
        df['SL'] = 0
        
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

        gt = DonchianTrend(
            df,
            pip_value,
            # use_spread=use_spread,
            # LOSS_FACTOR = stop_loss,
            # PROFIT_FACTOR = take_profit,
            # fixed_tp_sl=fixed_tp_sl,
            # trans_cost=trans_cost,
            # neg_multiplier=neg_multiplier,
            # rev=rev,
            # spread_limit=spread_limit,
            donchian_window_prev = prewindow
        )
        
        gt.run_test()


    return get_response(result)
