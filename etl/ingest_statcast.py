# --- REVISED ingest_statcast.py ---
from utils.warnings_config import suppress_warnings
suppress_warnings()
from pybaseball import statcast
import logging
from utils.r2_uploader import upload_df_to_r2 # <-- Import our new function

START_DATE = "2024-05-01"
END_DATE = "2024-05-07"
OBJECT_NAME = f"statcast_{START_DATE}_to_{END_DATE}.parquet" # <-- This is the filename in R2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_upload_statcast_data(start_date: str, end_date: str, object_name: str):
    logging.info(f"Fetching Statcast data from {start_date} to {end_date}...")
    try:
        df = statcast(start_dt=start_date, end_dt=end_date)
        logging.info(f"Successfully fetched {len(df)} records.")
        
        # Call the uploader function
        upload_df_to_r2(df, object_name)

    except Exception as e:
        logging.error(f"An error occurred during Statcast ETL: {e}")

if __name__ == "__main__":
    fetch_and_upload_statcast_data(START_DATE, END_DATE, OBJECT_NAME)






