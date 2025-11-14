import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

print("DEBUG: Running load.py from:", os.path.realpath(__file__))
print("DEBUG: GOOGLE_JSON_KEY_FILE_PATH =", os.getenv("GOOGLE_JSON_KEY_FILE_PATH"))


# === STEP 0: Load environment variables ===

# Get project root dynamically (works locally and in container)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Load .env file if running locally
load_dotenv(os.path.join(PROJECT_ROOT, "config/.env"), override=True)

# === CONFIGURATION ===
sqlite_db_path = os.path.join(PROJECT_ROOT, "products.db")
sqlite_table_name = "products"
bq_project = os.getenv("BQ_PROJECT", "daniel-grocery-project")
bq_dataset = "products_dataset"
bq_table = "products_2"

# Get credentials path from environment (GitHub Actions / Docker / local)
credentials_path = os.getenv("GOOGLE_JSON_KEY_FILE_PATH")

if not credentials_path or not os.path.exists(credentials_path):
    raise FileNotFoundError(
        f"❌ Google credentials file not found. Expected at: {credentials_path}\n"
        "Make sure GOOGLE_JSON_KEY_FILE_PATH is set correctly (e.g., /tmp/gcp-key.json in GitHub Actions)."
    )

print(f"✅ Using Google credentials from: {credentials_path}")

# === STEP 1: READ DATA FROM SQLITE ===
conn = sqlite3.connect(sqlite_db_path)
df = pd.read_sql_query(f"SELECT * FROM {sqlite_table_name}", conn)
conn.close()

print(f"Loaded {len(df)} rows from {sqlite_table_name} in SQLite.")

# === STEP 2: UPLOAD TO BIGQUERY ===
client = bigquery.Client.from_service_account_json(credentials_path, project=bq_project)
table_id = f"{bq_project}.{bq_dataset}.{bq_table}"

job = client.load_table_from_dataframe(df, table_id)
job.result()  # Wait for completion

print(f"✅ Successfully loaded {len(df)} rows into {table_id}.")
