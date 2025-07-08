from fastapi import FastAPI, Request, Response, HTTPException
from routes import anonymize, save_metadata
from fastapi.middleware.cors import CORSMiddleware
from firestore.firestore_client import get_firestore_client
import logging


app = FastAPI()  # creates a server
logger = logging.getLogger("uvicorn")

logger.setLevel(logging.INFO)  # set log level to INFO
logger.info("Starting FastAPI application...")

origins = [
    "http://localhost:8081",         # sviluppo: proxy React/Vite
    "http://localhost:3000",         # sviluppo: React puro
    "http://localhost:5173",         # sviluppo: Vite dev server
    "https://frontend-service-hclc243hba-ew.a.run.app",  # produzione: frontend
    "https://frontend-service-583549727222.europe-west1.run.app", # produzione: frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Origin", "Accept", "X-Requested-With", "Content-Type", "Access-Control-Request-Method", "Access-Control-Request-Headers", "Authorization", "authorization"],
)

app.include_router(anonymize.router)
app.include_router(save_metadata.router)

@app.get("/test-cors")
def test():
    return {"message": "CORS ok"}
