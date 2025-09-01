import pandas as pd
import logging
from utils.r2_uploader import upload_df_to_r2 

# --- Configuration ---
BASE_URL = "https://raw.githubusercontent.com/chadwickbureau/register/master/data/"
OBJECT_NAME = "player_map.parquet" 
REQUIRED_COLUMNS = ['key_mlbam', 'key_retro', 'name_first', 'name_last']
SHARDS = [str(i) for i in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_upload_player_map():
    """
    Downloads all 16 sharded Chadwick player register files, combines them,
    and uploads the result to R2 as a single Parquet file.
    """

    all_dfs = []
    logging.info("Starting download of 16 sharded player map files...")

    for shard in SHARDS:
        file_url = f"{BASE_URL}people-{shard}.csv"
        try:
            df = pd.read_csv(file_url, dtype={'key_mlbam': 'Int64'})
            all_dfs.append(df)
            logging.info(f"Successfully downloaded and read {file_url}")
        except Exception as e:
            logging.error(f"Failed to process file {file_url}: {e}")

    if not all_dfs:
        logging.error("No dataframes were downloaded. Aborting.")
        return

    master_df = pd.concat(all_dfs, ignore_index=True)
    logging.info(f"Combined files into a dataframe with {len(master_df)} total records.")

    # Filter and clean the combined data
    df_filtered = master_df[REQUIRED_COLUMNS].copy()
    df_cleaned = df_filtered.dropna(subset=['key_mlbam', 'key_retro'])
    df_cleaned['key_mlbam'] = df_cleaned['key_mlbam'].astype(int)

    # Call the uploader function instead of saving locally
    upload_df_to_r2(df_cleaned, OBJECT_NAME)

if __name__ == "__main__":
    fetch_and_upload_player_map()