import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from a different .env file
load_dotenv(dotenv_path="config/.env")

CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")
test_var = os.getenv("test_var")
print("CWD:", os.getcwd())


# Token endpoint
TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"

# # Data payload
# data = {
#     "grant_type": "client_credentials",
#     "scope": "product.compact"
# }

# # Make the POST request with HTTP Basic Auth
# response = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

# # Parse the JSON response
# if response.status_code == 200:
#     token_data = response.json()
# else:
#     print("Error:", response.status_code, response.text)
#     exit()

# # Query parameters to search for "chicken"
# params = {
#     "filter.term": "chicken",  # Search term
#     "filter.locationId": "01100002",  # Store location ID
#     "filter.limit": 5  # Limit the number of results
# }

# # Base URL for Kroger Products API
# url = "https://api.kroger.com/v1/products"

# # Headers (Authorization with Bearer token)
# headers = {
#     "Authorization": f"Bearer {token_data['access_token']}",
# }

# # Send GET request
# response = requests.get(url, headers=headers, params=params)

# product_id_list = []

# # Handle response
# if response.status_code == 200:
#     data = response.json()
#     if "data" in data and len(data["data"]) > 0:
#         print("\nProducts Found:")
#         for product in data["data"]:
#             product_name = product.get("description", "N/A")
#             product_id = product.get("productId", "N/A")
#             product_id_list.append(product_id)
#             print(f"Product Name: {product_name}")
#             print(f"Product ID: {product_id}")
#             print("-" * 40)
#     else:
#         print("No products found for the search term.")
# else:
#     print("❌ Error in GET request:", response.status_code, response.text)


# #print(product_id_list) # Print the list of product IDs

# print(data["data"])
# print("CLIENT_ID from os.getenv:", os.getenv("KROGER_CLIENT_ID"))