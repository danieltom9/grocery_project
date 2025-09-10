from datetime import datetime
from pipeline.ingestion.api_fetch import get_token, fetch_product
from pipeline.transformation.clean_prices import clean_product_data
from pipeline.validation.schema_check import validate_row
from pipeline.load.to_csv import save_to_csv
from pipeline.alerts.email_alerts import send_alert

items_to_track = {
    "Organic Whole Milk 1 Gallon": {"upc": "041496000145", "alert_price": 3.50},
    "White Bread 20oz": {"upc": "041496000238", "alert_price": 2.00}
}

def run():
    token = get_token()
    rows = []

    for name, info in items_to_track.items():
        raw = fetch_product(token, info["upc"])
        row = clean_product_data(raw, name, info["upc"])
        if row and validate_row(row):
            row["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row["alert_price"] = info["alert_price"]
            rows.append(row)

            if row["regular_price"] <= info["alert_price"]:
                send_alert(name, row["regular_price"], info["alert_price"])

    if rows:
        save_to_csv(rows)

if __name__ == "__main__":
    run()
