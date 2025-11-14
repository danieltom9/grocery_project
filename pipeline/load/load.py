import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

print("DEBUG: Running load.py from:", os.path.realpath(__file__))
print("DEBUG: GOOGLE_JSON_KEY_FILE_PATH =", os.getenv("GOOGLE_JSON_KEY_FILE_PATH"))

# === STEP 0: Load environment variables ===

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
load_dotenv(os.path.join(PROJECT_ROOT, "config/.env"), override=True)

# === CONFIGURATION ===
sqlite_db_path = os.path.join(PROJECT_ROOT, "products.db")
sqlite_table_name = "products"
bq_project = os.getenv("BQ_PROJECT", "daniel-grocery-project")
bq_dataset = "products_dataset"
bq_table = "products_2"

# === STEP 1: Resolve credentials path ===
credentials_path = os.getenv("GOOGLE_JSON_KEY_FILE_PATH")

# Strict validation — do NOT fallback to your Mac path
if not credentials_path:
    raise RuntimeError("❌ GOOGLE_JSON_KEY_FILE_PATH is not set in the environment.")

if not os.path.exists(credentials_path):
    raise FileNotFoundError(
        f"❌ Google credentials file does NOT exist at: {credentials_path}\n"
        "This means GitHub Actions failed to write /tmp/gcp-key.json.\n"
        "Fix: base64 encode your service account and decode it in the workflow."
    )

print(f"✅ Using Google credentials from: {credentials_path}")

# === STEP 2: READ DATA FROM SQLITE ===
conn = sqlite3.connect(sqlite_db_path)
df = pd.read_sql_query(f"SELECT * FROM {sqlite_table_name}", conn)
conn.close()

print(f"Loaded {len(df)} rows from {sqlite_table_name} in SQLite.")

# === STEP 3: UPLOAD TO BIGQUERY ===
client = bigquery.Client.from_service_account_json(credentials_path, project=bq_project)
table_id = f"{bq_project}.{bq_dataset}.{bq_table}"

job = client.load_table_from_dataframe(df, table_id)
job.result()

print(f"✅ Successfully loaded {len(df)} rows into {table_id}.")
