import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, Depends, APIRouter
import logging

logging.basicConfig(level=logging.INFO)

# Load Firebase service account credentials
if not firebase_admin._apps:
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if cred_path and os.path.exists(cred_path):
        # Ambiente locale: carica il file JSON dal percorso
        cred = credentials.Certificate(cred_path)
    else:
        # Ambiente Cloud Run: usa le Application Default Credentials
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)

# Dependency to verify Firebase token in Authorization header
async def verify_token(request: Request):
    if request.method == "OPTIONS":
        return  # skip auth per preflight
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization Header")

    token = auth_header.split(" ")[1]
    logging.info(f"Token ricevuto: {token}")  # Logging
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Errore verifica token Firebase: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
