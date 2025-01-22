from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def test_s3_storage():
    """
    Test the upload and retrieval of files using S3 storage in Django.
    """
    # File name and content for testing
    test_file_name = "test_upload.txt"
    test_file_content = b"This is a test file for S3 storage."

    # Upload the file to S3
    file_path = default_storage.save(test_file_name, ContentFile(test_file_content))
    print(f"File uploaded to: {file_path}")

    # Retrieve the URL of the uploaded file
    file_url = default_storage.url(file_path)
    print(f"File URL: {file_url}")

    # Verify the file URL works
    import requests
    response = requests.get(file_url)
    
    if response.status_code == 200 and response.content == test_file_content:
        print("Test successful: File uploaded and retrieved successfully!")
    else:
        print("Test failed: File content mismatch or URL inaccessible.")

if __name__ == "__main__":
    test_s3_storage()
