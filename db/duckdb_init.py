import duckdb
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "data" / "mlb.duckdb"
PARQUET_DIR = PROJECT_ROOT / "data" / "parquet"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    """
    Initializes the DuckDB database by dropping and recreating all views.
    """
    logging.info(f"Connecting to DB at {DB_FILE} to create views...")
    try:
        con = duckdb.connect(database=str(DB_FILE), read_only=False)

        # View 1: Statcast
        statcast_files = PARQUET_DIR / "statcast_*.parquet" 
        con.execute("DROP VIEW IF EXISTS v_statcast;")
        con.execute(f"CREATE VIEW v_statcast AS SELECT * FROM read_parquet('{str(statcast_files)}');")
        logging.info("View 'v_statcast' forcefully created.")

        # View 2: Lahman People
        lahman_file = PARQUET_DIR / "lahman_people.parquet"
        con.execute("DROP VIEW IF EXISTS v_lahman_people;")
        con.execute(f"CREATE VIEW v_lahman_people AS SELECT * FROM read_parquet('{str(lahman_file)}');")
        logging.info("View 'v_lahman_people' forcefully created.")
            
        # View 3: Player ID Map
        map_file = PARQUET_DIR / "player_map.parquet"
        con.execute("DROP VIEW IF EXISTS v_player_map;")
        con.execute(f"CREATE VIEW v_player_map AS SELECT * FROM read_parquet('{str(map_file)}');")
        logging.info("View 'v_player_map' forcefully created.")

        con.close()
        logging.info("Database connection closed.")

    except Exception as e:
        logging.error(f"An error occurred during database initialization: {e}")

if __name__ == "__main__":
    initialize_database()


