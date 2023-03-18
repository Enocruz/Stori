
import boto3
from botocore.exceptions import ClientError


def get_file(file_name: str):
    try:
        s3 = boto3.client("s3")
        file = s3.get_object(Bucket="files-public-transactions", Key=file_name)
        return file.get("Body") if file else None
    except ClientError:
        print(f"Unable to find file {file_name}")
        return None