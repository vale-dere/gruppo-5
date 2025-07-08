#what the server does when someone sends a POST to the /anonymize path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Response
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import numpy as np
import json
import os
import uuid
from auth.firebase_auth import verify_token
import google.auth
from google.auth.transport.requests import Request
import datetime
from datetime import timedelta
from storage.storage import upload_blob
from google.cloud import storage

from algorithms.k_anonymity import apply_k_anonymity
from algorithms.l_diversity import apply_l_diversity
from algorithms.t_closeness import apply_t_closeness
from algorithms.differential_privacy import apply_differential_privacy
from config.keywords import IDENTIFIER_KEYWORDS, SENSITIVE_KEYWORDS, QUASI_IDENTIFIER_KEYWORDS

router = APIRouter()

USE_GCS = True  # True --> Google Cloud Storage, False ---> local
GCS_BUCKET_NAME = "gruppo5-datasets"  # bucket GCS
GCS_FOLDER = "anonymized"  

@router.get("/protected")
async def protected_route(user_data=Depends(verify_token)):
    return {"message": "Accesso autorizzato!", "user_id": user_data['uid']}

# Creo cartella per salvare i file
OUTPUT_DIR = "generated_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_for_json(df):
    # Sostituisci inf con NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    # Sostituisci NaN con None
    df = df.where(pd.notnull(df), None)
    # Converti tipi float in oggetti per evitare problemi di serializzazione JSON
    for col in df.columns:
        if pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype(object)
    return df
''' PER ORA LO LASCIO QUI IL CODICE, POI CAPIAMO SE IMPLEMENTARLO O MENO
def fallback_quasi_identifiers(df: pd.DataFrame, top_n: int = 2) -> list[str]:
    # Colonne non identifier e non sensitive, con più di una modalità e non tutte uniche
    candidate_cols = [col for col in df.columns 
                      if df[col].nunique() > 1 and df[col].nunique() < len(df) and not pd.api.types.is_float_dtype(df[col])]
    # Se non ci sono candidate, torna vuoto
    if not candidate_cols:
        return []

    # Ordina per entropia decrescente (simile a fallback_sensitive_attr)
    entropies = {}
    for col in candidate_cols:
        counts = df[col].value_counts(normalize=True)
        entropy = -np.sum(counts * np.log2(counts + 1e-9))
        entropies[col] = entropy

    sorted_cols = sorted(entropies.items(), key=lambda x: x[1], reverse=True)
    selected = [col for col, _ in sorted_cols[:top_n]]
    return selected
'''
def fallback_sensitive_attr(df: pd.DataFrame, quasi_identifiers: list[str], top_n: int = 1) -> list[str]:
    """Se non si trova un attributo sensibile, sceglie come fallback il QI più variegato."""
    if not quasi_identifiers:
        return []

    # Calcola l'entropia di ciascun quasi-identificatore
    entropies = {}
    for col in quasi_identifiers:
        # Frequenza relativa delle modalità
        counts = df[col].value_counts(normalize=True)
        entropy = -np.sum(counts * np.log2(counts + 1e-9))  # log2 con epsilon per evitare log(0)
        entropies[col] = entropy

    # Ordina per entropia decrescente e prendi i top_n
    sorted_attrs = sorted(entropies.items(), key=lambda x: x[1], reverse=True)
    selected = [col for col, _ in sorted_attrs[:top_n]]

    print(f"[Fallback] Attributo sensibile selezionato automaticamente: {selected}")
    return selected


def classify_columns(df: pd.DataFrame):
    identifiers = []
    sensitive = []
    quasi_identifiers = []

    for col in df.columns:
        col_lower = col.lower().strip()

        # Identificatori diretti
        if any(k in col_lower for k in IDENTIFIER_KEYWORDS):
            identifiers.append(col)
            continue

        # Attributi sensibili
        if any(k in col_lower for k in SENSITIVE_KEYWORDS):
            sensitive.append(col)
            continue

        # QI per keyword
        if any(k in col_lower for k in QUASI_IDENTIFIER_KEYWORDS):
            quasi_identifiers.append(col)
            continue

        # QI per struttura numerica (es. anni, età)
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna()
            if not values.empty:
                if 0 <= values.min() <= 120 and values.max() <= 120:
                    quasi_identifiers.append(col)
                    continue
                if 1900 <= values.min() <= 2100 and values.max() <= 2100:
                    quasi_identifiers.append(col)
                    continue

    return identifiers, quasi_identifiers, sensitive

@router.get("/anonymize")
async def anonymize():
    return {"message": "Anonymization API is running. Use POST /anonymize to anonymize data."}

@router.post("/anonymize")
async def anonymize(
    user_data=Depends(verify_token),
    file: UploadFile = File(...),
    algorithm: str = Form(...),
    parameter: str = Form(...)
):
    print("File:", file.filename) # Debugging
    print("Tipo file ricevuto:", file.content_type) # Debugging

    # 1. Validazione tipo file
    if file.content_type not in ("text/csv", "application/json"):
        raise HTTPException(status_code=400, detail="Formato file non valido. Solo CSV o JSON.")

    # 2. Lettura e parsing del file
    try:
        content = await file.read()
        if file.content_type == "text/csv":
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_json(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella lettura del file: {str(e)}")

    print("initial dataset:", df ) # Debugging
   
    # 3. Determina quasi-identifiers e sensitive attributes dinamicamente
    identifiers, quasi_ids, sensitive_attr = classify_columns(df)
  
    if not quasi_ids: #da valutare se aggiungere anche qui fallback
        print("Nessun quasi-identificatore trovato nel dataset.")
        raise HTTPException(status_code=400, detail="Nessun quasi-identificatore trovato nel dataset.")

    if not sensitive_attr and (algorithm == "l-diversity" or algorithm == "t_closeness") :
        print("Nessun attributo sensibile trovato. Attivo fallback")
        sensitive_attr = fallback_sensitive_attr(df, quasi_ids)
        if not sensitive_attr:
            raise HTTPException(
                status_code=400,
                detail="Nessun attributo sensibile rilevato nel dataset, neanche con fallback. Impossibile procedere."
            )

    #debug
    print("Identificatori diretti:", identifiers)
    print("Attributi sensibili:", sensitive_attr)
    print("Quasi-identificatori:", quasi_ids)
    
    #rimozione identifdicatori diretti
    if identifiers:
        print("Rimozione colonne identificatrici:", identifiers)
        df.drop(columns=identifiers, inplace=True, errors='ignore')
    
    #Log finale delle colonne che restano nel dataset
    print("Colonne rimanenti dopo pulizia:", list(df.columns))

    # 4. Parsing e validazione parametro
    try:
        print(f"Parametro ricevuto: '{parameter}'")  # Debugging
        if algorithm in ["differential-privacy", "t-closeness"]:
            param = float(parameter)
        else:
            param = int(parameter)
    except ValueError:
        raise HTTPException(status_code=400, detail="Parametro non valido. Deve essere un numero.")

    # 5. Applica l’algoritmo
    result = None
    try:
        if algorithm == "k-anonymity":
            result = apply_k_anonymity(df, quasi_ids, param)
        elif algorithm == "l-diversity":
            result = apply_l_diversity(df, quasi_ids, sensitive_attr, param)
        elif algorithm == "t-closeness":
            result = apply_t_closeness(df, quasi_ids, sensitive_attr, param)        
        elif algorithm == "differential-privacy":
            result = apply_differential_privacy(df, param)
        else:
            raise HTTPException(status_code=400, detail="Algoritmo non supportato.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'applicazione dell'algoritmo: {str(e)}")

    # 6. Restituisce la preview
    print("Dataset dopo l'applicazione dell'algoritmo:", result) # Debugging
    result_clean = sanitize_for_json(result) #good practice to clean data before sending it back
    try:
        json.dumps(result_clean.head().to_dict(orient="records"))
        print("OK, il JSON si serializza")
    except Exception as e:
        print("Errore nella serializzazione JSON:", e)
    preview = result_clean.head().to_dict(orient="records")
    
    # 7. Salvataggio del file anonimizzato
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.csv"

    if USE_GCS:
        try:
            # Salva temporaneamente in memoria
            output_buffer = BytesIO()
            result.to_csv(output_buffer, index=False)
            output_buffer.seek(0)

            # Upload su Cloud Storage
            client = storage.Client()
            bucket = client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(f"{GCS_FOLDER}/{filename}")
            blob.upload_from_file(output_buffer, content_type="text/csv")

            # Ottieni credenziali e token da ADC (es. Cloud Run)
            credentials, project_id = google.auth.default()
            credentials.refresh(Request())  # Assicura che il token sia valido

            # Verifica che le credenziali contengano service_account_email e token
            service_account_email = getattr(credentials, "service_account_email", None)
            access_token = getattr(credentials, "token", None)

            if service_account_email and access_token:
                # Genera signed URL v4 valido per 15 minuti (inline = anteprima)
                expiration = datetime.timedelta(minutes=15)
                download_url = blob.generate_signed_url(
                    version="v4",
                    expiration=expiration,
                    method="GET",
                    response_disposition="inline",
                    service_account_email=service_account_email,
                    access_token=access_token,
                )
            else:
                raise ValueError("Credenziali non valide per la generazione del signed URL.")

            print(f"File caricato su GCS: gs://{GCS_BUCKET_NAME}/anonymized/{filename}")
            print(f"URL di download temporaneo: {download_url}")

        except Exception as e:
            print("Errore durante il salvataggio su GCS:", e)
            raise HTTPException(status_code=500, detail="Errore durante il salvataggio del file su GCS.")
    else:
        try:
            output_path = os.path.join(OUTPUT_DIR, filename)
            result.to_csv(output_path, index=False)
            download_url = f"http://localhost:8080/download/{file_id}"
            print(f"File anonimizzato salvato localmente in: {output_path}")
        except Exception as e:
            print("Errore durante il salvataggio locale:", e)
            raise HTTPException(status_code=500, detail="Errore durante il salvataggio locale.")

    return {
    "preview": preview,
    "data": result_clean.to_dict(orient="records"),  # Manda anche il dataset completo per salvarlo dopo
    "download_url": download_url,
    "download_file_id": file_id  # ID del file per il download
}

@router.get("/download/{file_id}")
async def download_anonymized_file(file_id: str, user_data=Depends(verify_token)):
    try:
        # Costruisci il nome del file
        filename = f"{file_id}.csv"
        blob_path = os.path.join(GCS_FOLDER, filename).replace("\\", "/") #cross-platform compatibilità

        # Inizializza il client GCS
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(blob_path)

        # Verifica che il file esista su GCS
        if not blob.exists():
            raise HTTPException(status_code=404, detail="File non trovato su GCS.")

        # Scarica il file come bytes
        file_bytes = blob.download_as_bytes()

        # Restituisci il contenuto come FileResponse (CORS-safe)
        return Response(
            content=file_bytes,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"'
            }
        )

    except Exception as e:
        print(f"Errore durante il download del file da GCS: {e}")
        raise HTTPException(status_code=500, detail="Errore durante il download del file.")
