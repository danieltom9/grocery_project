#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import argparse
import sqlite3
from datetime import datetime
from prefect.blocks.system import Secret

#DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "products.db")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DB_PATH = os.path.join(PROJECT_ROOT, "products.db")



# Load environment variables from a different .env file
load_dotenv(dotenv_path="config/.env", override=True)

CLIENT_ID = os.getenv("KROGER_CLIENT_ID") or Secret.load("kroger-client-id").get()
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET") or Secret.load("kroger-client-secret").get()

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

def create_database():
    """Create the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            product_id TEXT,
            product_name TEXT,
            price FLOAT,
            search_term TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(product_id, product_name, price, search_term):
    """Save a product to the SQLite database."""
    current_datetime = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (datetime, product_id, product_name, price, search_term)
        VALUES (?, ?, ?, ?, ?)
    """, (current_datetime, product_id, product_name, price, search_term))
    conn.commit()
    conn.close()

def search_products(search_term, location_id="01100002", limit=5):
    """Search for products using the Kroger API."""
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
                print("Saving:", product_id, product_name, price, search_term)
                save_to_database(product_id, product_name, price, search_term)
            print("\nProduct IDs:", product_id_list)
            print("Product Names:", product_name_list)
            print("Prices:", price_list)
        else:
            print("No products found for the search term.")
    else:
        print("❌ Error in GET request:", response.status_code, response.text)

if __name__ == "__main__":
    create_database()
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Search for products in the Kroger API.")
    parser.add_argument("search_term", nargs="+")
    args = parser.parse_args()
    
    # print statement to show parsed arguments
    print("Parsed arguments:", args.search_term)

    # Call the search function with the provided search term
    for term in args.search_term: 
        search_products(term)

