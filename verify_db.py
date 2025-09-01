import duckdb
from pathlib import Path
import sys

# --- Use an unambiguous, absolute path to the database file ---
PROJECT_ROOT = Path(__file__).resolve().parent
DB_FILE = PROJECT_ROOT / "data" / "mlb.duckdb"

print("-" * 50)
print(f"Attempting to inspect database file at: {DB_FILE}")

if not DB_FILE.exists():
    print(f"\nERROR: Database file not found at the specified path.")
    print("Please run `python -m db.duckdb_init` to create it.")
    sys.exit(1) # Exit the script with an error code

con = None
try:
    # Connect to the database file in read-only mode
    con = duckdb.connect(database=str(DB_FILE), read_only=True)
    print("\nSuccessfully connected to the database file.")
    
    # Execute the query to show all tables and views
    results = con.execute("SHOW TABLES;").fetchall()
    
    print("\nFound the following tables/views:")
    if results:
        for row in results:
            print(f"- {row[0]}")
    else:
        print("-> No tables or views found in the database.")

except Exception as e:
    print(f"\nAn ERROR occurred while inspecting the database: {e}")

finally:
    if con:
        con.close()
    print("-" * 50)