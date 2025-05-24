from fastapi import FastAPI
from routes import anonymize
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #creates a server

app.add_middleware( 
  CORSMiddleware,
  allow_origins=["http://localhost:5173","http://localhost:3000","http://localhost:8081"],  # porta React
  #allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(anonymize.router)