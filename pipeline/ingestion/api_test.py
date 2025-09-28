import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from a different .env file
load_dotenv(dotenv_path="config/.env")

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

# Token endpoint
TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"

# Data payload
data = {
    "grant_type": "client_credentials",
    "scope": "product.compact"
}

# Make the POST request with HTTP Basic Auth
response = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

# Parse the JSON response
if response.status_code == 200:
    token_data = response.json()
else:
    print("Error:", response.status_code, response.text)

# Query parameters (same as what I used in the curl command)
params = {
    #"filter.productId": "0001111041600",  # product ID
    "filter.locationId": "01100002",       # store location ID
    "filter.term": "chicken"  # Search term

}

# Base URL for Kroger Products API
url = "https://api.kroger.com/v1/products"

# Headers (Authorization with Bearer token)
headers = {
    "Authorization": f"Bearer {token_data['access_token']}",
}

# Send GET request
response = requests.get(url, headers=headers, params=params)

product_id_list = []
product_name_list = []
price_list = []


# Handle response
if response.status_code == 200:
    data = response.json()
    if "data" in data and len(data["data"]) > 0:
        print("\nProducts Found:")
        for product in data["data"]:
            product_name = product.get("description", "N/A")
            product_id = product.get("productId", "N/A")
            items = product.get("items", [])
            if items:
                price = items[0].get("price", {}).get("regular", "N/A")
                price_list.append(price)
            else:
                price = "N/A"
            product_id_list.append(product_id)
            product_name_list.append(product_name)
    else:
        print("No products found for the search term.")
else:
    print("❌ Error in GET request:", response.status_code, response.text)

response_text=response.json()

# Navigate into JSON structure
product = response_text["data"][0]          # first product
milk = product["description"]  # product description
item = product["items"][0]                  # first item
price = item["price"]["regular"]            # regular price

#print("Price:", price)
#print(f"The price of {milk} is: $", price)
print(product_id_list)
print(product_name_list)
print(price_list)


