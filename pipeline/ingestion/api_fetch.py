import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from a different .env file
load_dotenv(dotenv_path="config/secrets.env")

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

def get_token():
    '''Fetch access token from the Kroger API.'''
    url = "https://api.kroger.com/v1/connect/oauth2/token"
    data = {"grant_type": "client_credentials", "scope": "product.compact"}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)  # Debugging
    response.raise_for_status()
    return response.json()["access_token"]

def fetch_product(token, upc):
    '''Fetch product data from the Kroger API using the provided UPC.'''
    url = f"https://api.kroger.com/v1/products?filter.upc={upc}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print("Product Response Status Code:", response.status_code)
    print("Product Response Content:", response.text)  # Debugging
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    #Get access token
    token = get_token()
    print("Access Token:", token)
    
    #Fetch product data
    upc="0001111040101"
    product_data = fetch_product(token, upc) 

    # Step 3: Display product data
    if "data" in product_data and len(product_data["data"]) > 0:
        product = product_data["data"][0]  # Assuming the first product is the one we want
        print("\nProduct Details:")
        print(f"Name: {product.get('description', 'N/A')}")
        print(f"UPC: {product.get('upc', 'N/A')}")
        print(f"Brand: {product.get('brand', 'N/A')}")
        print(f"Category: {product.get('categories', ['N/A'])[0]}")
        print(f"Price: {product.get('items', [{}])[0].get('price', {}).get('regular', 'N/A')}")
    else:
        print("No product data found for the given UPC.")