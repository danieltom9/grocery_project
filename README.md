🛒 Grocery Product Analytics Pipeline

An end-to-end analytics engineering project that ingests product data from the Kroger API, applies structured transformations and data quality validation with dbt, loads curated models into BigQuery, and delivers business-ready insights through Looker Studio.

This project demonstrates modern data stack principles: modular modeling, automated data validation, cloud warehousing, and CI-driven orchestration.

🏗 Architecture

```mermaid
flowchart LR
    A[Kroger API] --> B[Python Extraction]
    B --> C[SQLite Raw Storage]
    C --> D[dbt Transform & Tests]
    D --> E[BigQuery Warehouse]
    E --> F[Looker Studio Dashboard]
    G[GitHub Actions] --> B
    G --> D
```

🚀 Pipeline Workflow

1. Extract raw grocery product data from the Kroger REST API using Python

2. Persist raw ingestion data in SQLite to simulate a staging layer

3. Transform and model data using dbt

4. Apply YAML schema tests to validate data quality

5. Deduplicate product_id values via SQL model

6. Enforce uniqueness constraints using dbt tests

7. Load curated models into BigQuery (products_dataset.products_2)

8. Power analytics dashboards in Looker Studio

9. Orchestrate the full workflow daily using GitHub Actions

🧠 Analytics Engineering Approach

- This project follows analytics engineering best practices:

- Clear separation between raw ingestion and analytics-ready models

- dbt-driven transformation layer

- Automated data quality validation

- Reproducible daily orchestration

- Warehouse-first modeling mindset

Data Validation Strategy

- YAML schema tests

- Explicit uniqueness validation on product_id

- SQL model to deduplicate source data before warehouse load

- Automated test execution during scheduled runs

🛠 Tech Stack

- Python 3.10

- SQLite (raw staging layer)

- dbt (transformation & data quality)

- Google BigQuery (cloud data warehouse)

- GitHub Actions (CI/CD orchestration)

- Looker Studio (analytics & visualization)

🔄 Orchestration & Automation

- Fully automated daily pipeline using GitHub Actions

- End-to-end execution including:

    - API extraction

    - Transformation

    - dbt tests

    - Warehouse load

- Designed for repeatability and production-style execution

📦 Warehouse Output

BigQuery

- Dataset: products_dataset

- Table: products_2

The final table contains validated, deduplicated, analytics-ready grocery product data suitable for BI consumption.

📊 Outcome

This project demonstrates:

    - End-to-end data pipeline ownership

    - Data modeling discipline using dbt

    - Automated data validation workflows

    - Cloud warehouse integration

    - CI-based orchestration

    - Delivery of BI-ready datasets

🔮 Future Enhancements

- Incremental models for performance optimization

- Warehouse partitioning & clustering

- dditional analytics marts

- Infrastructure as code (Terraform)

- Data freshness monitoring

