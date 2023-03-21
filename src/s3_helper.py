
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "files-public-transactions"

def get_file(file_name: str):
    """
    Retrieves the file from the bucket and returns
    its contents
    """
    try:
        s3 = boto3.client("s3")
        file = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
        return file.get("Body") if file else None
    except ClientError:
        print(f"Unable to find file {file_name}")
        return None