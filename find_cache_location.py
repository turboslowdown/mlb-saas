from pybaseball import cache

print("Finding the pybaseball cache directory location...")
try:
    # The config object holds the path to the cache directory
    cache_directory = cache.config.CACHE_DIR
    print("-" * 50)
    print(f"Pybaseball cache directory is: {cache_directory}")
    print("-" * 50)
    print("\nPlease manually delete this entire folder using the 'rm -rf' command.")

except Exception as e:
    print(f"Could not determine the cache location automatically: {e}")