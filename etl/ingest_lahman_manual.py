import pandas as pd
from pathlib import Path
import logging
from utils.r2_uploader import upload_df_to_r2 # <-- Import the uploader

# --- Configuration ---
# This local path is still needed to read the source CSV
LAHMAN_DATA_DIR = Path("/Users/josephndigiovanni/Downloads/baseballdatabank-master")
INPUT_FILE = LAHMAN_DATA_DIR / "core" / "People.csv"
OBJECT_NAME = "lahman_people.parquet" # <-- The destination filename in R2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_and_upload_local_lahman():
    """
    Reads the locally downloaded Lahman 'People.csv' file and uploads it
    to R2 as a Parquet file.
    """
    if not INPUT_FILE.exists():
        logging.error(f"Input file not found: {INPUT_FILE}")
        return

    logging.info(f"Reading local Lahman data from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
        logging.info(f"Successfully read {len(df)} player records.")
        
        # Call the uploader function instead of saving locally
        upload_df_to_r2(df, OBJECT_NAME)

    except Exception as e:
        logging.error(f"An error occurred during local Lahman processing: {e}")

if __name__ == "__main__":
    process_and_upload_local_lahman()