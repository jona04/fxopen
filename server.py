from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.quotehistory_collection import quotehistoryCollection
from api.fxopen_api import FxOpenApi
from api.web_options import get_options
from dateutil import parser
import http

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    quotehistoryCollection.LoadQuotehistoryDB()
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


@app.get("/api/prices-candle/{pair}/{granularity}/{count}")
def get_quotehistory(pair: str, granularity: str, count:int):
    api = FxOpenApi()
    df_candles = api.get_candles_df(
        pair=pair, count=count*-1, granularity=granularity
    )

    return get_response(df_candles.to_dict("list"))

@app.get("/api/prices-candle/{pair}/{granularity}/{date_f}")
def get_quotehistory(pair: str, granularity: str, date_f: str):
    api = FxOpenApi()
    dfr = parser.parse(date_f)
    # dfr = parser.parse("2024-08-12T04:00:00Z")
    df_candles = api.get_candles_df(
        pair=pair, count=-10, granularity=granularity, date_f=dfr
    )

    return get_response(df_candles.to_dict("list"))


@app.get("/api/last-complete-candle/{pair}/{granularity}")
def last_complete_candle(pair: str, granularity: str):
    api = FxOpenApi()
    df_candle = api.last_complete_candle(pair=pair, granularity=granularity)

    return get_response(df_candle)
