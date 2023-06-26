
from fastapi import FastAPI, Body, Header, Request
from pprint import pprint
from os import environ
from app.ParseMessage import OrderMesssage
from app.BybitFutures import NBybitFuture
from app.BinanceFutures import NBinanceFuture
from enum import Enum
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from jwt import decode

BINANCE_API_KEY = environ.get("BINANCE_API_KEY", None)
BINANCE_API_SECRET = environ.get("BINANCE_API_SECRET", None)
BYBIT_API_KEY = environ.get("BYBIT_API_KEY", None)
BYBIT_API_SECRET = environ.get("BYBIT_API_SECRET", None)
PROXY_API_KEY = environ.get("PROXY_API_KEY", None)
PROXY_API_SECRET = environ.get("PROXY_API_SECRET", None)
TESTNET = bool(environ.get("TESTNET", 0))
LEVERAGE = float(environ.get("LEVERAGE", 1))

um_futures_client = NBinanceFuture(api_key=BINANCE_API_KEY, 
                                   secret=BINANCE_API_SECRET, 
                                   url="https://testnet.binance.vision/api")
bybit_client = NBybitFuture(
    api_key=BYBIT_API_KEY,
    secret=BYBIT_API_SECRET,
    testnet=TESTNET
)

class Side(Enum):
    Sell = "SELL"
    Buy = "BUY"
    
    def __str__(self) -> str:
        return self.value

    
class Action(Enum):
    OpenShort = "OS"
    OpenLong = "OL"
    CloseShort = "CS"
    CloseLong = "CL"
    CloseShortOpenLong = "CSOL"
    CloseLongOpenShort = "CLOS"
    
    def __str__(self) -> str:
        return self.value
    

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



def verify_jwt(jwt_str, secret, api_key):
    try:
        print("JWT :: ", jwt_str)
        result = decode(jwt_str, secret, algorithms=["HS256"])
        print("Decode ::", result)
        return api_key == result.get("apiKey", None)
    except Exception as e:
        return False

#####################################################
#### API ###
@app.get("/")
async def main(request: Request):
    user_ip = request.headers.get('CF-Connecting-IP', request.client.host)
    country = request.headers.get('CF-IPCountry', "nowhere")
    return {"message": f"Hello  {user_ip} from {country} -- TESTNET : {TESTNET} {datetime.now()}"}

@app.get("/health")
async def check_health():
    return {"message": f"Still Alive -- TESTNET : {TESTNET} {datetime.now()}"}

@app.post("/alert-hook")
async def alert_hook(body: str = Body(..., media_type='text/plain'), jwt: str | None = Header(default=None)):
    order = OrderMesssage(body)
    client = um_futures_client if order.exchange == "BINANCE" else bybit_client
    print()
    pprint(order.json)
    print()
    
    if not verify_jwt(jwt, PROXY_API_SECRET, PROXY_API_KEY):
        return {"status": 403, "message" : "Authentication Error"}
    
    try:
        if order.message == f"{Action.CloseShortOpenLong}":
            print("--------- CLOSE SHORT -->  OPEN LONG ---------")
            client.close_short(symbol=order.symbol)
            client.open_long(symbol=order.symbol, percent=LEVERAGE)
            
        elif order.message == f"{Action.CloseLongOpenShort}":
            print("--------- CLOSE LONG -->  OPEN SHORT ---------")
            client.close_long(symbol=order.symbol)
            client.open_short(symbol=order.symbol, percent=LEVERAGE)  
            
        elif order.message == f"{Action.CloseShort}":
            print("--------- CLOSE SHORT ---------")
            client.close_short(symbol=order.symbol)
        
        elif order.message == f"{Action.CloseLong}":
            print("--------- CLOSE LONG ---------")
            client.close_long(symbol=order.symbol)
            
        else:
            if order.side == Side.Sell.value:
                print("--------- OPEN SHORT ---------")
                client.open_short(symbol=order.symbol, percent=LEVERAGE)  
            else:
                print("--------- OPEN LONG ---------")
                client.open_long(symbol=order.symbol, percent=LEVERAGE)
                
    except Exception as e:
        print(e)
        print("---"*10)
        print()
        return {"status": 500, "message" : f"{e}"}
    
    print("---"*10)
    print()
    return {"status": 200, "message" : "OK"}


#####################################################


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)


