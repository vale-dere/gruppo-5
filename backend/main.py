from fastapi import FastAPI
from routes import anonymize
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #creates a server

app.add_middleware( #va qui?
  CORSMiddleware,
  #allow_origins=["http://localhost:5173","http://localhost:3000"],  # porta React
  allow_origins=["*"],  # porta React TEST PURPOSES, DA ELIMINARE
  #allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(anonymize.router)