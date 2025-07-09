from fastapi import FastAPI, Request, Response, HTTPException
from routes import anonymize
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()  # creates a server

origins = [
    "http://localhost:8081",         # development: React/Vite proxy
    "http://localhost:3000",         # development: pure React
    "http://localhost:5173",         # development: Vite dev server
    "https://frontend-service-hclc243hba-ew.a.run.app",  # production: frontend
    "https://frontend-service-583549727222.europe-west1.run.app", # production: frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Origin", "Accept", "X-Requested-With", "Content-Type", "Access-Control-Request-Method", "Access-Control-Request-Headers", "Authorization", "authorization"],
)

app.include_router(anonymize.router)

@app.get("/test-cors")
def test():
    return {"message": "CORS ok"}
