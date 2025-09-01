# Import the warning suppressor FIRST
from utils.warnings_config import suppress_warnings
suppress_warnings()

import pandas as pd
from pybaseball.lahman import people
from pathlib import Path
import logging

# --- Configuration ---
OUTPUT_DIR = Path("data/parquet")
OUTPUT_FILE = OUTPUT_DIR / "lahman_people.parquet"

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_save_lahman_people():
    """
    Fetches the Lahman 'people' table containing player biographical data
    and saves it as a Parquet file.
    """
    logging.info("Fetching Lahman 'people' data...")
    try:
        # The people() function directly returns a pandas DataFrame
        df = people()

        if df.empty:
            logging.warning("No data returned from Lahman 'people' table.")
            return

        logging.info(f"Successfully fetched {len(df)} player records.")
        
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save to Parquet
        df.to_parquet(OUTPUT_FILE, index=False)
        logging.info(f"Lahman 'people' data successfully saved to {OUTPUT_FILE}")

    except Exception as e:
        logging.error(f"An error occurred during Lahman data fetching: {e}")

if __name__ == "__main__":
    fetch_and_save_lahman_people()