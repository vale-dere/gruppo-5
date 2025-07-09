from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Response
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import numpy as np
import json
import os
import uuid
from auth.firebase_auth import verify_token
import google.auth
from google.auth.transport.requests import Request
import datetime
from datetime import timedelta
from storage.storage import upload_blob
from google.cloud import storage
from firestore.firestore_client import get_firestore_client
import logging

from algorithms.k_anonymity import apply_k_anonymity
from algorithms.l_diversity import apply_l_diversity
from algorithms.t_closeness import apply_t_closeness
from algorithms.differential_privacy import apply_differential_privacy
from config.keywords import IDENTIFIER_KEYWORDS, SENSITIVE_KEYWORDS, QUASI_IDENTIFIER_KEYWORDS

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter()

USE_GCS = True  # True --> Google Cloud Storage, False ---> local
GCS_BUCKET_NAME = "gruppo5-datasets"  # GCS bucket
GCS_FOLDER = "anonymized"

# Create folder for saving files only if using local storage.
OUTPUT_DIR = "generated_files"
if not USE_GCS:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_for_json(df):
    # Replace inf with NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    # Replace NaN with None
    df = df.where(pd.notnull(df), None)
    # Convert float types to object to avoid JSON serialization issues
    for col in df.columns:
        if pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype(object)
    return df

def fallback_sensitive_attr(df: pd.DataFrame, quasi_identifiers: list[str], top_n: int = 1) -> list[str]:
    """If no sensitive attribute is found, fallback to the most varied QI."""
    if not quasi_identifiers:
        return []

    # Calculate entropy for each quasi-identifier
    entropies = {}
    for col in quasi_identifiers:
        counts = df[col].value_counts(normalize=True)
        entropy = -np.sum(counts * np.log2(counts + 1e-9))  # log2 with epsilon to avoid log(0)
        entropies[col] = entropy

    # Sort by descending entropy and take top_n
    sorted_attrs = sorted(entropies.items(), key=lambda x: x[1], reverse=True)
    selected = [col for col, _ in sorted_attrs[:top_n]]

    logger.info(f"[Fallback] Automatically selected sensitive attribute: {selected}")
    return selected

def classify_columns(df: pd.DataFrame):
    identifiers = []
    sensitive = []
    quasi_identifiers = []

    for col in df.columns:
        col_lower = col.lower().strip()

        # Direct identifiers
        if any(k in col_lower for k in IDENTIFIER_KEYWORDS):
            identifiers.append(col)
            continue

        # Sensitive attributes
        if any(k in col_lower for k in SENSITIVE_KEYWORDS):
            sensitive.append(col)
            continue

        # QI by keyword
        if any(k in col_lower for k in QUASI_IDENTIFIER_KEYWORDS):
            quasi_identifiers.append(col)
            continue

        # QI by numeric structure (e.g., years, age)
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna()
            if not values.empty:
                if 0 <= values.min() <= 120 and values.max() <= 120:
                    quasi_identifiers.append(col)
                    continue
                if 1900 <= values.min() <= 2100 and values.max() <= 2100:
                    quasi_identifiers.append(col)
                    continue

    return identifiers, quasi_identifiers, sensitive

@router.get("/anonymize")
async def anonymize():
    return {"message": "Anonymization API is running. Use POST /anonymize to anonymize data."}

@router.post("/anonymize")
async def anonymize(
    user_data=Depends(verify_token),
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    parameter: str = Form(...)
):
    logger.info(f"File: {file.filename}")  # Debugging
    logger.info(f"Received file type: {file.content_type}")  # Debugging

    # 1. File type validation
    if file.content_type not in ("text/csv", "application/json"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV or JSON allowed.")

    # 2. Read and parse the file
    try:
        content = await file.read()
        if file.content_type == "text/csv":
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_json(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    # 3. Dynamically determine quasi-identifiers and sensitive attributes
    identifiers, quasi_ids, sensitive_attr = classify_columns(df)

    if not quasi_ids:
        logger.error("No quasi-identifiers found in the dataset.")
        raise HTTPException(status_code=400, detail="No quasi-identifiers found in the dataset.")

    if not sensitive_attr and (algorithm == "l-diversity" or algorithm == "t_closeness"):
        logger.warning("No sensitive attribute found. Activating fallback.")
        sensitive_attr = fallback_sensitive_attr(df, quasi_ids)
        if not sensitive_attr:
            raise HTTPException(
                status_code=400,
                detail="No sensitive attribute detected in the dataset, not even with fallback. Cannot proceed."
            )

    # Debug
    logger.info(f"Direct identifiers: {identifiers}")
    logger.info(f"Sensitive attributes: {sensitive_attr}")
    logger.info(f"Quasi-identifiers: {quasi_ids}")

    # Remove direct identifiers
    if identifiers:
        logger.info(f"Removing identifier columns: {identifiers}")
        df.drop(columns=identifiers, inplace=True, errors='ignore')

    # 4. Parse and validate parameter
    try:
        logger.info(f"Received parameter: '{parameter}'")  # Debugging
        if algorithm in ["differential-privacy", "t-closeness"]:
            param = float(parameter)
        else:
            param = int(parameter)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid parameter. Must be a number.")

    # 5. Apply the algorithm
    result = None
    try:
        if algorithm == "k-anonymity":
            result = apply_k_anonymity(df, quasi_ids, param)
        elif algorithm == "l-diversity":
            result = apply_l_diversity(df, quasi_ids, sensitive_attr, param)
        elif algorithm == "t-closeness":
            result = apply_t_closeness(df, quasi_ids, sensitive_attr, param)
        elif algorithm == "differential-privacy":
            result = apply_differential_privacy(df, param)
        else:
            raise HTTPException(status_code=400, detail="Unsupported algorithm.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying algorithm: {str(e)}")

    # 6. Return the preview
    result_clean = sanitize_for_json(result)
    try:
        json.dumps(result_clean.head().to_dict(orient="records"))
        logger.info("JSON serialization successful")
    except Exception as e:
        logger.error(f"Error in JSON serialization: {e}")
    preview = result_clean.head().to_dict(orient="records")

    # 7. Save the anonymized file
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.csv"

    if USE_GCS:
        try:
            # Save temporarily in memory
            output_buffer = BytesIO()
            result.to_csv(output_buffer, index=False)
            output_buffer.seek(0)

            # Upload to Cloud Storage
            client = storage.Client()
            bucket = client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(f"{GCS_FOLDER}/{filename}")
            blob.upload_from_file(output_buffer, content_type="text/csv")

            # Get credentials and token from ADC (e.g., Cloud Run)
            credentials, project_id = google.auth.default()
            credentials.refresh(Request())  # Ensure token is valid

            # Check that credentials contain service_account_email and token
            service_account_email = getattr(credentials, "service_account_email", None)
            access_token = getattr(credentials, "token", None)

            if service_account_email and access_token:
                # Generate signed URL v4 valid for 15 minutes (inline = preview)
                expiration = datetime.timedelta(minutes=15)
                download_url = blob.generate_signed_url(
                    version="v4",
                    expiration=expiration,
                    method="GET",
                    response_disposition="inline",
                    service_account_email=service_account_email,
                    access_token=access_token,
                )
                firestore_client = get_firestore_client()
                firestore_client.collection("datasets").add({
                    "user_id": user_data["uid"],
                    "file_id": file_id,
                    "filename": filename,
                    "algorithm": algorithm,
                    "param": param,
                    "timestamp": datetime.datetime.utcnow(),
                    "gcs_path": f"gs://{GCS_BUCKET_NAME}/{GCS_FOLDER}/{filename}"
                })
            else:
                raise ValueError("Invalid credentials for generating signed URL.")

            logger.info(f"File uploaded to GCS: gs://{GCS_BUCKET_NAME}/anonymized/{filename}")
            logger.info(f"Temporary download URL: {download_url}")

        except Exception as e:
            logger.error(f"Error saving to GCS: {e}")
            raise HTTPException(status_code=500, detail="Error saving file to GCS.")
    else:
        try:
            output_path = os.path.join(OUTPUT_DIR, filename)
            result.to_csv(output_path, index=False)
            download_url = f"http://localhost:8080/download/{file_id}"
            logger.info(f"Anonymized file saved locally at: {output_path}")
        except Exception as e:
            logger.error(f"Error in local saving: {e}")
            raise HTTPException(status_code=500, detail="Error in local saving.")

    return {
        "preview": preview,
        "data": result_clean.to_dict(orient="records"),  # Also send the full dataset for later saving
        "download_url": download_url,
        "download_file_id": file_id  # File ID for download
    }

@router.get("/download/{file_id}")
async def download_anonymized_file(file_id: str, user_data=Depends(verify_token)):
    try:
        # Build the file name
        filename = f"{file_id}.csv"
        blob_path = os.path.join(GCS_FOLDER, filename).replace("\\", "/")  # cross-platform compatibility

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(blob_path)

        # Check that the file exists on GCS
        if not blob.exists():
            raise HTTPException(status_code=404, detail="File not found on GCS.")

        # Download the file as bytes
        file_bytes = blob.download_as_bytes()

        # Return the content as FileResponse (CORS-safe)
        return Response(
            content=file_bytes,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"'
            }
        )

    except Exception as e:
        logger.error(f"Error downloading file from GCS: {e}")
        raise HTTPException(status_code=500, detail="Error downloading file.")
