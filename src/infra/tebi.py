import boto3
from botocore.client import Config
import os

def get_tebi_client():
    print("TEBI_ENDPOINT", os.getenv("TEBI_ENDPOINT"))
    print("TEBI_ACCESS_KEY", os.getenv("TEBI_ACCESS_KEY"))
    print("TEBI_SECRET_KEY", os.getenv("TEBI_SECRET_KEY"))
    print("TEBI_BUCKET", os.getenv("TEBI_BUCKET"))
    
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("TEBI_ENDPOINT", "https://s3.tebi.io"),
        aws_access_key_id=os.getenv("TEBI_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("TEBI_SECRET_KEY"),
        region_name="global",
        config=Config(signature_version="s3v4"),
    )
