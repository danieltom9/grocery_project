import subprocess

# Step 1: Ingest raw data
subprocess.run(["python", "ingestion/ingest_sales_data.py"], check=True)

# Step 2: Load data to warehouse
subprocess.run(["python", "loading/load_to_warehouse.py"], check=True)

# Step 3: Run dbt transformations
subprocess.run(["dbt", "run", "--project-dir", "transformation/dbt_project"], check=True)

# Step 4: Optional - dbt tests
subprocess.run(["dbt", "test", "--project-dir", "transformation/dbt_project"], check=True)
