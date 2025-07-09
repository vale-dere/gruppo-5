import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, Depends, APIRouter
import logging

logging.basicConfig(level=logging.INFO)

# Load Firebase service account credentials
if not firebase_admin._apps:
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if cred_path and os.path.exists(cred_path):
        # Local environment: load the JSON file from the path
        cred = credentials.Certificate(cred_path)
    else:
        # Cloud Run environment: use Application Default Credentials
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)

# Dependency to verify Firebase token in Authorization header
async def verify_token(request: Request):
    if request.method == "OPTIONS":
        return  # skip auth for preflight
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization Header")

    token = auth_header.split(" ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logging.error(f"Firebase token verification error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
