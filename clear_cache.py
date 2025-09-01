from pybaseball import cache

print("Attempting to purge the pybaseball cache...")
try:
    cache.purge()
    print("Pybaseball cache purged successfully!")
    print("You can now re-run the ingestion script.")
except Exception as e:
    print(f"An error occurred while clearing the cache: {e}")