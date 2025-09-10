import requests
from requests.auth import HTTPBasicAuth
import os

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

def get_token():
    url = "https://api.kroger.com/v1/connect/oauth2/token"
    data = {"grant_type": "client_credentials", "scope": "product.compact"}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_product(token, upc):
    url = f"https://api.kroger.com/v1/products?filter.upc={upc}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()