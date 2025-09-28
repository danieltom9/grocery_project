#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from a different .env file
load_dotenv(dotenv_path="config/.env", override=True)

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")

# Token endpoint
TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"

def get_access_token():
    #Fetching the access token from the Kroger API
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }
    response = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        print("Error fetching token:", response.status_code, response.text)
        exit()


def search_products(search_term, location_id="01100002", limit=5):
    #Function to search for products using the Kroger API
    url = "https://api.kroger.com/v1/products"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    params = {
        "filter.term": search_term,
        "filter.locationId": location_id,
        "filter.limit": limit
    }
    response = requests.get(url, headers=headers, params=params)  
    if response.status_code == 200: 
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            product_id_list = []
            product_name_list = []
            price_list = []
            #print("\nProducts Found:")
            for product in data["data"]:
                product_name = product.get("description", "N/A")
                product_id = product.get("productId", "N/A")
                items = product.get("items", [])
                if items:
                    price = items[0].get("price", {}).get("regular", "N/A")
                else:
                    price = "N/A"
                product_id_list.append(product_id)
                product_name_list.append(product_name)
                price_list.append(price)
                #print(f"Product Name: {product_name}")
                #print(f"Product ID: {product_id}")
                #print(f"Price: {price}")
                #print("-" * 40)
            print("\nProduct IDs:", product_id_list)
            print("Product Names:", product_name_list)
            print("Prices:", price_list)
        else:
            print("No products found for the search term.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Search for products in the Kroger API.")
    parser.add_argument("search_term",nargs="+")
    args = parser.parse_args()

    print("Parsed arguments:", args.search_term)

    #parser = argparse.ArgumentParser(description="Process an argument specified multiple times.")
    #parser.add_argument('-i', '--input', action='append', help='Specify multiple input items.')

    #args = parser.parse_args()  


    # Call the search function with the provided search term
    for term in args.search_term: 
        search_products(term)

