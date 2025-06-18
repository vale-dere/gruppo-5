import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, Depends, APIRouter


# Load Firebase service account credentials
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "firebase-service-account.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


# Dependency to verify Firebase token in Authorization header
async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization Header")

    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

'''
# Public route to verify backend is running
# doesn't allow upload, download or access to sensitive data. Useful for testing, health checks and api discovery
@app.get("/")
def root():
    return {"message": "Anonymizer backend is running!"}
'''