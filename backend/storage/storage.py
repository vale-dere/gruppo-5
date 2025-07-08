from google.cloud import storage
import os

def get_storage_client():
    # GOOGLE_APPLICATION_CREDENTIALS must be set
    return storage.Client()

def upload_blob(bucket_name: str, source_file_path: str, destination_blob_name: str):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    # Can return the public URL or the blob ID if needed
    return f"gs://{bucket_name}/{destination_blob_name}"
