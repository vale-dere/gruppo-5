from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Depends
import pandas as pd
import firebase_admin
from firebase_admin import credentials, auth
import os

app = FastAPI()

# Load Firebase service account credentials
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "firebase-service-account.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Dependency to verify Firebase token in Authorization header
async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Public route to verify backend is running
# doesn't allow upload, download or access to sensitive data. Useful for testing, health checks and api discovery
@app.get("/")
def root():
    return {"message": "Anonymizer backend is running!"}

# Private route that requires Firebase-authenticated user
@app.post("/upload")
async def upload(file: UploadFile = File(...), user_data: dict = Depends(verify_token)): #dict necessary to authentication
    df = pd.read_csv(file.file)
    return {
        "columns": df.columns.tolist(),
        "rows": len(df),
        "uploaded_by": user_data.get("email")
    }

# Optional extra route for testing authentication
@app.get("/private")
async def private_route(user_data: dict = Depends(verify_token)): #to manage middleware and access controls to route
    # This route is only accessible to authenticated users, verify_token must be true 
    return {"message": f"Hello {user_data.get('email')}, you're authenticated!"}
