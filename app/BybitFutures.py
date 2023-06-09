from pybit.unified_trading import HTTP
from pprint import pprint
from enum import Enum

class Category(Enum):
    linear = "linear"

class AccoutType(Enum):
    unitfied = "UNIFIED"


class Side(Enum):
    Sell = "Sell"
    Buy = "Buy"

class Type(Enum):
    Market = "Market"
    Limit = "LIMIT"

class NBybitFuture:
    
    def __init__(self, api_key, secret, testnet=True):
        url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
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

        return self.c_pprint(result["result"]["list"][0], name="Balance", filter_keys=["totalAvailableBalance", "totalMarginBalance"])
         
    
    def get_ticker(self, symbol="ARBUSDT"):
        """_summary_

        Args:
            symbol (str, optional): _description_. Defaults to "ARBUSDT".

        Returns:
            ============================== ARBUSDT ==============================

            {'ask1Price': '1.1665',
            'bid1Price': '1.1664',
            'indexPrice': '1.1635',
            'markPrice': '1.1666',
            'symbol': 'ARBUSDT'}

            ============================================================
        """
        result = self.client_ss.get_tickers(
            category=Category.linear.value,
            symbol=symbol,
        )
        
        if result.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {result.get('retMsg', '')} ")
            return {}

        return self.c_pprint(result["result"]["list"][0], name=symbol, filter_keys=["symbol", "ask1Price", "bid1Price", "markPrice", "indexPrice"])
    
    def get_position(self, symbol="ARBUSDT"):
        response = self.client_ss.get_positions(
            category=Category.linear.value,
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
        qty = self.get_position(symbol=symbol).get("size", 0)
        print("qty")
        if qty in [0, "0"]:
            print(f"[ INFO  ] Bybit : No Open order ")
            return {}
        
        response = self.client_ss.place_order(
            category=Category.linear.value,
            symbol=symbol,
            side=Side.Sell.value,
            orderType=Type.Market.value,
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
        qty = self.get_position(symbol=symbol).get("size", 0)
        print("qty")
        if qty in [0, "0"]:
            print(f"[ INFO  ] Bybit : No Open order ")
            return {}
        
        response = self.client_ss.place_order(
            category=Category.linear.value,
            symbol=symbol,
            side=Side.Buy.value,
            orderType=Type.Market.value,
            qty=qty,
            timeInForce="GTC",
            takeProfit="0",
            stopLoss="0",
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
    
    
    def open_long(self, qty=0, percent=1, symbol="ARBUSDT"):
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
        
        bid_price = float(self.get_ticker(symbol=symbol).get("bid1Price", 0))
        
        if bid_price == 0:
            print(f"[INFO  ] Bybit : cannot get bid1Price of {symbol}")
            return {}
        
        if qty == 0:
            qty = balance *  percent / bid_price
        
        response = self.client_ss.place_order(
            category=Category.linear.value,
            symbol=symbol,
            side=Side.Buy.value,
            orderType=Type.Market.value,
            qty=f'{qty: 0.2f}',
            timeInForce="GTC",
            takeProfit="0",
            stopLoss="0",
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
        
        
        
    def open_short(self, qty=0, percent=1, symbol="ARBUSDT"):
        balance = float(self.get_balance().get("totalAvailableBalance", 0))
        if balance == 0:
            print(f"[INFO  ] Bybit : Balance is 0")
            return {}
        
        bid_price = float(self.get_ticker(symbol=symbol).get("ask1Price", 0))
        
        if bid_price == 0:
            print(f"[INFO  ] Bybit : cannot get bid1Price of {symbol}")
            return {}
        
        if qty == 0:
            qty = balance *  percent / bid_price
        
        response = self.client_ss.place_order(
            category=Category.linear.value,
            symbol=symbol,
            side=Side.Sell.value,
            orderType=Type.Market.value,
            qty=f'{qty: 0.2f}',
            timeInForce="GTC",
            takeProfit="0",
            stopLoss="0",
        ) 
        
        if response.get("retMsg", None) != "OK": 
            print(f"[ INFO  ] Bybit : {response.get('retMsg', '')} ")
            return {}

        return self.c_pprint(response["result"], name=f"[ {symbol} ] OPEN ORDER", filter_keys=[])
    
  
def main():
    from os import environ
    SYMBOL = "ARBUSDT"
    n_bybit_client = NBybitFuture(api_key=environ["BYBIT_API_KEY"], secret=environ["BYBIT_API_SECRET"])
    # n_bybit_client.open_long(symbol=SYMBOL)
    n_bybit_client.get_balance()

    
    # n_bybit_client.get_position(symbol=SYMBOL)
    
    # n_bybit_client.close_short(symbol=SYMBOL)

if __name__ == "__main__":
    main()