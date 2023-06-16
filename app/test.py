import httpx
from os import environ
import jwt
from enum import Enum
import secrets
import random

class Action(Enum):
    OpenShort = "OS"
    OpenLong = "OL"
    CloseShort = "CS"
    CloseLong = "CL"
    CloseShortOpenLong = "CSOL"
    CloseLongOpenShort = "CLOS"
    
    def __str__(self) -> str:
        return self.value


order = {
    "message" : "CLOS - SAR"
}

def main_send_request():
    data = "symbol = SUIUSDT.P, exchange = BYBIT, side = buy, message = CS, size = 0, price = 1.1255"
    # base_url = "https://testnet-webhook-ewdxkehvuq-an.a.run.app"
    base_url = "http://localhost"
    # base_url = "https://proxyserver-ewdxkehvuq-an.a.run.app"
    # base_url = "http://34.143.142.93"

    REQUEST_URL = f"{base_url}/alert-hook"

    with httpx.Client() as client:
        # headers = {
        #     "Content-Type": "text/plain; charset=UTF-8",
        #     "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcGlLZXkiOiJXa2ZNSl8talloQTlKRmtaQ0RBMXZGSHIifQ.52qTKQ7nw8kGEy8lrHAix-agSxKMadZ3_pwnLVwNxmo"
        # }
        headers = {
            "Content-Type": "text/plain; charset=UTF-8",
            "jwt": "fdsfdsfdsfdsf"
        }
        r = client.post(REQUEST_URL, headers=headers, data=data)

    print(r)
    print(r.json())

def generate_api_key(n=5):
    index = random.randint(0, n-4)
    return [ secrets.token_urlsafe(18) for _ in range(n) ][index]

def generate_api_scecret(n=5):
    index = random.randint(0, n-4)
    return [ secrets.token_hex(18) for _ in range(n) ][index]

def create_jwt(api_key, api_secret):
    return jwt.encode({"apiKey": api_key}, api_secret, algorithm="HS256")

def verify_jwt(jwt_str, api_key, api_secret):
    return jwt.decode(jwt_str, api_secret, algorithms=["HS256"])


def main_generate_jwt():
    API_KEY = generate_api_key()
    API_SC = generate_api_scecret()
    print(API_KEY)
    print(API_SC)
    jwt_str = create_jwt(API_KEY, API_SC)
    print(jwt_str)
    print(verify_jwt(jwt_str, API_KEY, API_SC))



if __name__ == "__main__":
    # main_generate_jwt()
    main_send_request()