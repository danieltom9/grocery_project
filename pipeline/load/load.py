import pandas as pd
from dotenv import load_dotenv
import sqlite3
from google.cloud import bigquery
import os

# Get project root dynamically
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Load .env from project root
load_dotenv(os.path.join(PROJECT_ROOT, "config/.env"), override=True)



# === CONFIGURATION ===
'''sqlite_db_path = "/Users/danieltom/Desktop/daniel grocery project/products.db"'''
'''sqlite_db_path = "/app/products.db"'''
sqlite_db_path = os.path.join(PROJECT_ROOT, "products.db")
sqlite_table_name = "products"
bq_project = "daniel-grocery-project"
bq_dataset = "products_dataset"
bq_table = "products_2"
'''credentials_path = os.getenv("GOOGLE_JSON_KEY_FILE_PATH")'''
credentials_path = os.getenv("GOOGLE_JSON_KEY_FILE_PATH", "/app/config/gcp-key.json")



# === STEP 1: READ DATA FROM SQLITE ===
conn = sqlite3.connect(sqlite_db_path)
df = pd.read_sql_query(f"SELECT * FROM {sqlite_table_name}", conn)
conn.close()

print(f"Loaded {len(df)} rows from {sqlite_table_name} in SQLite.")

# === STEP 2: UPLOAD TO BIGQUERY ===
client = bigquery.Client.from_service_account_json(credentials_path, project=bq_project)
table_id = f"{bq_project}.{bq_dataset}.{bq_table}"

job = client.load_table_from_dataframe(df, table_id)

job.result()  # Waits for the job to finish

print(f"✅ Successfully loaded {len(df)} rows into {table_id}.")

 