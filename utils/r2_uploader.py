import os
import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import logging

load_dotenv()

# --- R2 Configuration ---
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

# The R2 endpoint URL is specific to your account ID
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"

# Setup the S3 client for R2
s3_client = boto3.client(
    service_name='s3',
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name='auto',
)

def upload_df_to_r2(df: pd.DataFrame, object_name: str):
    """
    Converts a pandas DataFrame to a Parquet file in memory and uploads it to R2.

    Args:
        df: The pandas DataFrame to upload.
        object_name: The desired filename/key in the R2 bucket (e.g., 'statcast.parquet').
    """
    if df.empty:
        logging.warning(f"DataFrame is empty. Skipping upload for {object_name}.")
        return

    logging.info(f"Preparing to upload '{object_name}' to R2 bucket '{BUCKET_NAME}'...")
    try:
        # Create an in-memory buffer
        parquet_buffer = BytesIO()
        
        # Write the DataFrame to the in-memory buffer as a Parquet file
        df.to_parquet(parquet_buffer, index=False)
        
        # Reset the buffer's cursor to the beginning
        parquet_buffer.seek(0)
        
        # Upload the in-memory file to R2
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=object_name,
            Body=parquet_buffer.read()
        )
        logging.info(f"Successfully uploaded {object_name} to R2.")
    
    except Exception as e:
        logging.error(f"Failed to upload {object_name} to R2: {e}")