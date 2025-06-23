from google.cloud import storage
import os

def get_storage_client():
    # Assicurati di avere GOOGLE_APPLICATION_CREDENTIALS impostato
    return storage.Client()

def upload_blob(bucket_name: str, source_file_path: str, destination_blob_name: str):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    # Puoi restituire l'URL pubblico o l'ID del blob, se serve
    return f"gs://{bucket_name}/{destination_blob_name}"
