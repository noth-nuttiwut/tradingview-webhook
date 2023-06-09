
from fastapi import FastAPI, Body
from pprint import pprint
from os import environ
from ParseMessage import OrderMesssage
from BybitFutures import NBybitFuture
from BinanceFutures import NBinanceFuture
from enum import Enum
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

BINANCE_API_KEY = environ["BINANCE_API_KEY"]
BINANCE_API_SECRET = environ["BINANCE_API_SECRET"]
BYBIT_API_KEY = environ["BYBIT_API_KEY"]
BYBIT_API_SECRET = environ["BYBIT_API_SECRET"]

um_futures_client = NBinanceFuture(api_key=BINANCE_API_KEY, 
                                   secret=BINANCE_API_SECRET, 
                                   url="https://testnet.binance.vision/api")
bybit_client = NBybitFuture(
    api_key=BYBIT_API_KEY,
    secret=BYBIT_API_SECRET,
)

class Side(Enum):
    Sell = "SELL"
    Buy = "BUY"
    
class Action(Enum):
    OpenShort = "OS"
    OpenLong = "OL"
    CloseShort = "CS"
    CloseLong = "CL"
    
    

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#####################################################
#### API ###
@app.get("/")
async def root():
    return {"message": f"Hello World -- {datetime.now()}"}

@app.get("/health")
async def check_health():
    return {"message": f"Still Alive -- {datetime.now()}"}

@app.post("/alert-hook")
async def alert_hook(body: str = Body(..., media_type='text/plain')):
    order = OrderMesssage(body)
    client = um_futures_client if order.exchange == "BINANCE" else bybit_client
    print()
    
    if order.message == "CS":
        print("--------- CLOSE SHORT ---------")
        client.close_short(symbol=order.symbol)
    
    elif order.message == "CL":
        print("--------- CLOSE LONG ---------")
        client.close_long(symbol=order.symbol)
    else:
        if order.side == Side.Sell.value:
            print("--------- OPEN SHORT ---------")
            client.open_short(symbol=order.symbol)  
        else:
            print("--------- OPEN LONG ---------")
            client.open_long(symbol=order.symbol)
    pprint(order.json)
    print("---"*10)
    print()
    return {"status": 200, "message" : "OK"}


#####################################################


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8008)
    
