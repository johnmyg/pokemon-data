# type: ignore
from datetime import datetime, timedelta
from dotenv import load_dotenv
import boto3
import os

load_dotenv()


def load_links(filepath: str = "data/links.txt") -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]
    return links


def get_yesterday_dates():
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%b %-d, %Y")
    filename_date = yesterday.strftime("%Y-%m-%d")
    return formatted_date, filename_date


def upload_file_to_s3(file_name, object):
    s3 = boto3.client("s3")
    bucket_name = os.getenv("BUCKET_NAME")

    try:
        s3.upload_file(file_name, bucket_name, object)
        print(f"Uploaded {file_name} to s3://{bucket_name}/{object}")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
