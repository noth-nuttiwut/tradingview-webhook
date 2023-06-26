from pybit.unified_trading import HTTP
from pprint import pprint
from enum import Enum

class Category(Enum):
    Linear = "linear"
    Inverse = "inverse"
    
    def __str__(self) -> str:
        return self.value

class AccoutType(Enum):
    unitfied = "UNIFIED"
    
    def __str__(self) -> str:
        return self.value


class Side(Enum):
    Sell = "Sell"
    Buy = "Buy"
    
    def __str__(self) -> str:
        return self.value

class Type(Enum):
    Market = "Market"
    Limit = "LIMIT"
    
    def __str__(self) -> str:
        return self.value

class NBybitFuture:
    
    def __init__(self, api_key, secret, testnet=True):
        self.client_ss = HTTP(
        testnet=testnet,
        api_key=api_key,
        api_secret=secret,
    )
        
    def c_pprint(self, dictionary, filter_keys=[], name=""):
        if name:
            print("=="*15, name, "=="*15)
        else:
            print("=="*30)
        
        print()
        if filter_keys:
            new_dict = { k : v for k, v in dictionary.items() if k in filter_keys}
            pprint(new_dict)
            print()
            print("=="*30)
            return new_dict
        
        pprint(dictionary)
        print("=="*30)
        return dictionary
        
        

    def get_balance(self):
        """_summary_

        Returns:
           ============================== Balance ==============================

            {'totalAvailableBalance': '10002.2795', 'totalMarginBalance': '10002.2795'}

            ============================================================
        """
        result = self.client_ss.get_wallet_balance(
            accountType=AccoutType.unitfied.value,
            coin="USDT,USDC",
        )

        if result.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {result.get('retMsg', '')} ")
            return {}

        filter_keys = ["totalAvailableBalance", "totalMarginBalance", "totalPerpUPL", "totalInitialMargin", "totalMaintenanceMargin"]
        return self.c_pprint(result["result"]["list"][0], name="Balance", filter_keys=filter_keys)
         
    
    def get_ticker(self, symbol="ARBUSDT"):
        """_summary_

        Args:
            symbol (str, optional): _description_. Defaults to "ARBUSDT".

        Returns:
            ============================== ARBUSDT ==============================

            {'a': [["16638.64", "0.008479"]],
            'b': [["16638.27", "0.305749"]],
            'ts': '1672765737733',
            'symbol': 'ARBUSDT'}

            ============================================================
        """
        result = self.client_ss.get_orderbook(
            category=f"{Category.Linear}",
            symbol=symbol,
            limit=10
        )
        """
        Response 

        {
            "retCode": 0,
            "retMsg": "OK",
            "result": {
                "s": "BTCUSDT",
                "a": [
                    [
                        "16638.64",
                        "0.008479"
                    ]
                ],
                "b": [
                    [
                        "16638.27",
                        "0.305749"
                    ]
                ],
                "ts": 1672765737733,
                "u": 5277055
            },
            "retExtInfo": {},
            "time": 1672765737734
        }
        """
        
        if result.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {result.get('retMsg', '')} ")
            return {}

        return self.c_pprint(result["result"], name=symbol, filter_keys=["s", "a", "b", "ts"])
    
    def get_position(self, symbol="ARBUSDT"):
        response = self.client_ss.get_positions(
            category=f"{Category.Linear}",
            symbol=symbol,
        )

        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}
        
        return self.c_pprint(response["result"]["list"][0], name=symbol, filter_keys=["symbol", "size", "positionValue", "unrealisedPnl"])
    
    
    def close_long(self, qty=0, percent=1, symbol="ARBUSDT"):
        """_summary_

        Args:
            qty (int, optional): _description_. Defaults to 0.
            percent (int, optional): _description_. Defaults to 1.
            symbol (str, optional): _description_. Defaults to "ARBUSDT".

        Returns:
            {'result': {'orderId': '37a25ec3-e2fe-4d8f-8d0b-b347df20838b',
                        'orderLinkId': ''},
            'retCode': 0,
            'retExtInfo': {},
            'retMsg': 'OK',
            'time': 1686130540125}
        """
        qty = self.get_position(symbol=symbol).get("size", "0").replace(" ", "")
        print("qty :: ", qty)
        if qty in [0, "0"]:
            print(f"[ INFO  ] Bybit : No Open order ")
            return {}
        
        response = self.client_ss.place_order(
            category=f"{Category.Linear}",
            symbol=symbol,
            side=f"{Side.Sell}",
            orderType=f"{Type.Market}",
            qty=qty,
            timeInForce="GTC",
            takeProfit="0",
            stopLoss="0",
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
    
    
    def close_short(self, qty=0, percent=1, symbol="ARBUSDT"):
        """_summary_

        Args:
            qty (int, optional): _description_. Defaults to 0.
            percent (int, optional): _description_. Defaults to 1.
            symbol (str, optional): _description_. Defaults to "ARBUSDT".

        Returns:
            {'result': {'orderId': '37a25ec3-e2fe-4d8f-8d0b-b347df20838b',
                        'orderLinkId': ''},
            'retCode': 0,
            'retExtInfo': {},
            'retMsg': 'OK',
            'time': 1686130540125}
        """
        qty = self.get_position(symbol=symbol).get("size", "0").replace(" ", "")
        if qty in [0, "0"]:
            print(f"[ INFO  ] Bybit : No Open order ")
            return {}
        
        response = self.client_ss.place_order(
            category=f"{Category.Linear}",
            symbol=symbol,
            side=f"{Side.Buy}",
            orderType=f"{Type.Market}",
            qty=qty,
            timeInForce="GTC",
            takeProfit="0",
            stopLoss="0",
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
    
    
    def open_long(self, qty=0, percent=1, symbol="ARBUSDT", max_loss=250, order_size=0):
        """_summary_

        Args:
            qty (int, optional): _description_. Defaults to 0.
            percent (int, optional): _description_. Defaults to 1.
            symbol (str, optional): _description_. Defaults to "ARBUSDT".

        Returns:
            {'result': {'orderId': '37a25ec3-e2fe-4d8f-8d0b-b347df20838b',
                        'orderLinkId': ''},
            'retCode': 0,
            'retExtInfo': {},
            'retMsg': 'OK',
            'time': 1686130540125}
        """
        balance = float(self.get_balance().get("totalAvailableBalance", 0))
        if balance == 0:
            print(f"[INFO  ] Bybit : Balance is 0")
            return {}
        
        bid_price = float(self.get_ticker(symbol=symbol).get("b", [[0, 0]])[0][0])
        
        if bid_price == 0:
            print(f"[INFO  ] Bybit : cannot get bid1Price of {symbol}")
            return {}
        
        if qty == 0 and order_size == 0:
            qty = round((balance *  percent) / bid_price, 2)
        
        elif qty == 0 and order_size > 0:
            qty = round(order_size / bid_price, 2)
        
        # Calculate stop loss
        stop_loss_price = (balance - max_loss) / qty
        response = self.client_ss.place_order(
            category=f"{Category.Linear}",
            symbol=symbol,
            side=f"{Side.Buy}",
            orderType=f"{Type.Market}",
            qty=f'{qty:0.2f}',
            timeInForce="GTC",
            takeProfit="0",
            stopLoss=f'0',
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
        
        
        
    def open_short(self, qty=0, percent=1, symbol="ARBUSDT", max_loss=250, order_size=0):
        balance = float(self.get_balance().get("totalAvailableBalance", 0))
        if balance == 0:
            print(f"[INFO  ] Bybit : Balance is 0")
            return {}
        
        bid_price = float(self.get_ticker(symbol=symbol).get("a", [[0, 0]])[0][0])
        
        if bid_price == 0:
            print(f"[INFO  ] Bybit : cannot get bid1Price of {symbol}")
            return {}
        
        if qty == 0 and order_size == 0:
            qty = round( (balance *  percent) / bid_price, 2)
        
        elif qty == 0 and order_size > 0:
            qty = round( order_size / bid_price, 2)
            
        # Calculate stop loss
        stop_loss_price = (balance + max_loss) / qty
        
        response = self.client_ss.place_order(
            category=f"{Category.Linear}",
            symbol=symbol,
            side=f"{Side.Sell}",
            orderType=f"{Type.Market}",
            qty=f'{qty:0.2f}',
            timeInForce="GTC",
            takeProfit="0",
            stopLoss=f'0',
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
  
def main():
    from os import environ
    SYMBOL = "ARBUSDT"
    n_bybit_client = NBybitFuture(api_key=environ["BYBIT_API_KEY"], secret=environ["BYBIT_API_SECRET"])

    n_bybit_client.close_long(symbol=SYMBOL)
    

    
if __name__ == "__main__":
    main()