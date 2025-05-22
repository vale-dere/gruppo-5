from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO
# from algorithms.k_anonymity import apply_k_anonymity  # Commento reale

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],  # porta React
  allow_methods=["*"],
  allow_headers=["*"],
)

# MOCK: una funzione dummy che non fa nulla di serio
def apply_k_anonymity(df, quasi_identifiers, k):
    # per ora semplicemente ritorno il df originale
    return df

@app.post("/anonymize")
async def anonymize(file: UploadFile = File(...), k: int = 2):
    # Controllo tipo
    if file.content_type not in ("text/csv", "application/json"):
        raise HTTPException(400, "File non valido")
    content = await file.read()
    # Carico il DataFrame
    if file.content_type == "text/csv":
        df = pd.read_csv(BytesIO(content))
    else:
        df = pd.read_json(BytesIO(content))
    # Applico mock di k-anonymity
    quasi_ids = [col for col in df.columns if col in ("age", "zipcode")]
    anonymized = apply_k_anonymity(df, quasi_ids, k)
    # Ritorno i primi 5 record come anteprima
    preview = anonymized.head().to_dict(orient="records")
    return {"preview": preview}
