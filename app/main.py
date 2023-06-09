
from fastapi import FastAPI, Body
from pprint import pprint
from os import environ
# from secretcode import F_API_KEY, F_API_SC, ByBit_KEY2, ByBit_SC2
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


# site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
# scheduler = SchedulerAdmin.bind(site)
# site.mount_app(app)

# mail_handler = MailHandler()


#####################################################
#### API ###
@app.get("/")
async def root():
    print("Check Bybit :: ")
    print(bybit_client.get_balance())
    return {"message": f"Hello World -- {datetime.now()}"}

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




#####################################################
### JOB SCHEDULE
# @scheduler.scheduled_job('interval', seconds=15)
# def check_email():
#     now = datetime.now()
#     print("[INFO ] CheckE-Mail ...", now)
#     mail_handler.read_mail(last_checked=now)
#     print("[INFO ] Done . ")


# @app.on_event("startup")
# async def startup():
#     # Start the scheduled task scheduler
#     scheduler.start()

#####################################################

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8008)
    
    
    
# curl -H 'Content-Type: text/plain; charset=utf-8' -d '' -X POST http://127.0.0.1:8008/alert-hook