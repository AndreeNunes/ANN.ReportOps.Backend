import os

import boto3
from botocore.client import Config


def _setting(*names, default=None):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


def get_bucket_name():
    return _setting("S3_BUCKET", "BUCKET", "TEBI_BUCKET")


def get_s3_client():
    endpoint = _setting("S3_ENDPOINT", "ENDPOINT", "TEBI_ENDPOINT")
    access_key = _setting("S3_ACCESS_KEY_ID", "ACCESS_KEY_ID", "TEBI_ACCESS_KEY")
    secret_key = _setting("S3_SECRET_ACCESS_KEY", "SECRET_ACCESS_KEY", "TEBI_SECRET_KEY")
    region = _setting("S3_REGION", "REGION", "AWS_DEFAULT_REGION", default="auto")
    url_style = _setting("S3_URL_STYLE", "AWS_S3_URL_STYLE", default="virtual")

    missing = [
        name
        for name, value in (
            ("S3_ENDPOINT", endpoint),
            ("S3_ACCESS_KEY_ID", access_key),
            ("S3_SECRET_ACCESS_KEY", secret_key),
            ("S3_BUCKET", get_bucket_name()),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"Configuração de storage ausente: {', '.join(missing)}")

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": url_style},
        ),
    )


get_tebi_client = get_s3_client
