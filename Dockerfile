FROM prefecthq/prefect:3.4.23-python3.10

WORKDIR /app

# Copy your flow code
COPY . /app
COPY products.db /app/products.db


# Install dependencies
RUN pip install -r requirements.txt


# Entry point for Prefect
CMD ["python", "pipeline/orchestration/run_pipeline.py"]
