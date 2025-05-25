#what the server does when someone sends a POST to the /anonymize path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd
from io import BytesIO
from algorithms.anonymization import (
    apply_differential_privacy,
    apply_k_anonymity,
    apply_l_diversity,
    apply_t_closeness
)

router = APIRouter()

@router.post("/anonymize")
async def anonymize(
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

    # 3. Determina le quasi-identifiers
    quasi_ids = [col for col in df.columns if col in ("age", "zipcode")]

    # 4. Parsing e validazione parametro
    try:
        if algorithm == "differential-privacy":
            param = float(parameter)
        else:
            param = int(parameter)
    except ValueError:
        raise HTTPException(status_code=400, detail="Parametro non valido. Deve essere un numero.")

    # 5. Applica l’algoritmo
    try:
        if algorithm == "k-anonymity":
            result = apply_k_anonymity(df, quasi_ids, param)
        elif algorithm == "l-diversity":
            result = apply_l_diversity(df, quasi_ids, "disease", param)
        elif algorithm == "t-closeness":
            result = apply_t_closeness(df, quasi_ids, "disease", param)
        elif algorithm == "differential-privacy":
            result = apply_differential_privacy(df, param)
        else:
            raise HTTPException(status_code=400, detail="Algoritmo non supportato.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'applicazione dell'algoritmo: {str(e)}")

    # 6. Restituisce la preview
    preview = result.head().to_dict(orient="records")
    return {"preview": preview}
