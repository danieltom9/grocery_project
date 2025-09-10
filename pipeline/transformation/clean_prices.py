import pandas as pd

def clean_product_data(raw_data, product_name, upc):
    items = raw_data.get("data", [])
    if not items:
        return None

    item = items[0]["items"][0]
    return {
        "name": product_name,
        "upc": upc,
        "regular_price": item["price"]["regular"],
        "promo_price": item["price"].get("promo", None)
    }