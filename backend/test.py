import boto3
from botocore.exceptions import ClientError

# AWS credentials and configurations (directly provided here, avoid in production)
AWS_ACCESS_KEY_ID = "AKIA2S2Y4I2T2SK4HRX5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "diginfluancer"
AWS_S3_REGION_NAME = "ap-south-1"
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"


def list_files_in_s3_bucket():
    """List files in the specified S3 bucket."""
    try:
        # Initialize a session using your provided credentials and region
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME,
        )

        # List objects in the specified S3 bucket
        response = s3_client.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME)

        if "Contents" in response:
            print(f"Files in bucket '{AWS_STORAGE_BUCKET_NAME}':")
            for obj in response["Contents"]:
                print(f" - {obj['Key']}")
        else:
            print(f"No files found in the bucket '{AWS_STORAGE_BUCKET_NAME}'.")

    except ClientError as e:
        print(f"An error occurred: {e}")


def main():
    list_files_in_s3_bucket()


if __name__ == "__main__":
    main()
