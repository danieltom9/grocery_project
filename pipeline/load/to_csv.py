import pandas as pd
import os

CSV_FILE = "data/warehouse/kroger_prices.csv"

def save_to_csv(rows):
    df = pd.DataFrame(rows)
    os.makedirs("data/warehouse", exist_ok=True)
    df.to_csv(CSV_FILE, mode="a", index=False, header=not os.path.exists(CSV_FILE))
    print(f"Saved {len(rows)} rows to {CSV_FILE}")