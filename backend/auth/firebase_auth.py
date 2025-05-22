from fastapi import Request, HTTPException
from firebase_admin import auth

''' DA SCOMMENTARE DOPO AVER AVUTO FILE JSON
# Load Firebase service account credentials (serve davvero?)
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
'''
# Placeholder function for token verification
async def verify_token(request: Request):
    return {"email": "dev@example.com"}  # fake user info for now

# Public route to verify backend is running
# doesn't allow upload, download or access to sensitive data. Useful for testing, health checks and api discovery
@app.get("/")
def root():
    return {"message": "Anonymizer backend is running!"}