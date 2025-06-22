from fastapi import FastAPI, Request, Response, HTTPException
from routes import anonymize, save_metadata
from fastapi.middleware.cors import CORSMiddleware
from firestore.firestore_client import get_firestore_client
import logging


app = FastAPI()  # creates a server
logger = logging.getLogger("uvicorn")

origins = [
    "http://localhost:8080",         # sviluppo: proxy cloudrun
    "http://127.0.0.1:8080",         # sviluppo: proxy cloudrun
    "http://localhost:8081",         # sviluppo: proxy React/Vite
    "http://localhost:3000",         # sviluppo: React puro
    "http://localhost:5173",         # sviluppo: Vite dev server
    "https://frontend-service-hclc243hba-ew.a.run.app",  # produzione
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:8080",         # sviluppo: proxy cloudrun
    "http://127.0.0.1:8080",         # sviluppo: proxy cloudrun
    "http://localhost:8081",         # sviluppo: proxy React/Vite
    "http://localhost:3000",         # sviluppo: React puro
    "http://localhost:5173",         # sviluppo: Vite dev server
    "https://frontend-service-hclc243hba-ew.a.run.app",  # produzione
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
''' gestione richieste OPTIONS per CORS
@app.middleware("http")
async def options_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        origin = request.headers.get("origin", "*")
        req_headers = request.headers.get("access-control-request-headers", "")
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": req_headers,
            "Access-Control-Allow-Credentials": "true"
        }
        return Response(status_code=200, headers=headers)
    return await call_next(request)
'''
app.include_router(anonymize.router)

app.include_router(save_metadata.router)

@app.get("/test-cors")
def test():
    return {"message": "CORS ok"}
