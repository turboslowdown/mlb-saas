import duckdb
from pathlib import Path
import pandas as pd
import logging
import numpy as np

# --- USE ABSOLUTE PATHS ---
PROJECT_ROOT = Path(__file__).parent.parent
DB_FILE = PROJECT_ROOT / "data" / "mlb.duckdb"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_query(sql_query: str) -> list[dict]:
    """
    Connects to the DuckDB database and executes a given SQL query.

    Args:
        sql_query: The SQL query string to execute.

    Returns:
        A list of dictionaries, where each dictionary represents a row.
        Returns an empty list if an error occurs or no data is found.
    """
    if not DB_FILE.exists():
        logging.error(f"Database file not found at {DB_FILE}. Please run `python -m db.duckdb_init`.")
        return []

    con = None
    try:
        # Connect in read-only mode for safety in an API context
        con = duckdb.connect(database=str(DB_FILE), read_only=True)
        logging.info(f"Executing query: {sql_query}")
        
        results_df = con.execute(sql_query).fetchdf()
        
        # Replace all occurrences of NaN (which is not valid JSON) with None (which becomes null).
        results_df_cleaned = results_df.replace({np.nan: None})
        
        # Convert the cleaned DataFrame to a list of dictionaries
        return results_df_cleaned.to_dict('records')

    except Exception as e:
        logging.error(f"An error occurred while executing query: {e}")
        return []
    finally:
        if con:
            con.close()