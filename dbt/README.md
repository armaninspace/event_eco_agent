# dbt Starter Project

This folder contains a small dbt + DuckDB semantic-layer starter.

## Setup

Install dependencies:

```bash
pip install dbt-core dbt-duckdb duckdb
```

Copy the example profile to your local dbt profile location or set `DBT_PROFILES_DIR`:

```bash
cd dbt/event_eco_semantic
export DBT_PROFILES_DIR=$PWD
cp profiles.example.yml profiles.yml
dbt debug
dbt run
dbt test
```

The starter mart joins county-week sports exposure to Womply county outcomes. Students can extend it with CBSA models, statistics-ready marts, and metric definitions.
