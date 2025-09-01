# Baseball Data MVP (Project: HotCorner)

This project is a minimum viable product (MVP) for a baseball data platform that allows for natural language querying of MLB statistics.

## Tech Stack

- **ETL:** Python, Pybaseball, Pandas
- **Database:** DuckDB (reading from Parquet files)
- **API:** FastAPI
- **LLM:** DeepSeek / OpenAI
- **Frontend:** Next.js (planned)

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd mlb-saas
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the initial data ingestion:**
    ```bash
    python etl/ingest_statcast.py
    ```
    This will create a Parquet file in the `data/parquet/` directory.

## Project Structure

- `data/parquet/`: Stores processed data ready for querying.
- `etl/`: Python scripts for fetching and transforming data.
- `utils/`: Helper modules, like configuration and warning suppression.
- `db/`: DuckDB initialization scripts and schema definitions.
- `api/`: The FastAPI backend for serving queries.
- `frontend/`: The Next.js user interface.