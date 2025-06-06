#what the server does when someone sends a POST to the /anonymize path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd
from io import BytesIO

from algorithms.k_anonymity import apply_k_anonymity
from algorithms.l_diversity import apply_l_diversity
from algorithms.t_closeness import apply_t_closeness
from algorithms.differential_privacy import apply_differential_privacy

router = APIRouter()

@router.get("/anonymize")
async def anonymize():
    return {"message": "Anonymization API is running. Use POST /anonymize to anonymize data."}

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
    quasi_ids_list = [
    "age", "birthdate", "year_of_birth", "date_of_birth",
    "zipcode", "postal_code", "zip", "postcode",
    "city", "town", "municipality",
    "state", "province", "region", "gender", "sex",
    "race", "ethnicity","marital_status", "maritalstatus",
    "occupation", "job_title", "profession",
    "education", "education_level", "degree",
    "phone_number", "telephone", "email_domain", "email",
    "address", "street", "street_address","country",
    "household_size", "family_size", "num_children",
    "nationality", "language", "income", "salary", "financial_status",]
    quasi_ids = [col for col in df.columns if col.lower() in quasi_ids_list] # c'è un modo per farlo più dinamico e generico?
    #quasi_ids = [col.lower() for col in df.columns if col.lower() in quasi_ids_list] se voglio che la listadi quasi_ids sia minuscola

    sensitive_data_list = ["disease", "diagnosis", "medical_condition", "health_status", "disability", "condition",
    "mental_health", "physical_health", "treatment", "medication", "therapy",
    "surgery", "genetic_data", "genome", "hereditary_condition",
    "biometric_data", "fingerprint", "retina_scan", "face_recognition", "voice_pattern",
    "sexual_orientation", "sexual_preference", "sex_life",
    "religion", "religious_belief", "faith", "creed",
    "political_opinion", "political_affiliation", "party_membership",
    "philosophical_belief", "moral_belief", "ideology",
    "union_membership", "labor_union", "trade_union",
    "criminal_record", "criminal_history", "offense", "conviction",
    "ethnicity", "racial_origin", "skin_color", "tribal_affiliation",
    "HIV_status", "STD_status", "cancer_type", "chronic_disease",
    "pregnancy_status", "fertility", "reproductive_health",
    "insurance_number", "social_security_number", "tax_id",
    "citizenship_status", "immigration_status", "asylum_status"]
    sensitive_attr = [col for col in df.columns if col.lower() in sensitive_data_list]

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
    preview = result.to_dict(orient="records")
    return {"preview": preview}

#codice generato ma non controllato per ottenere lista di quasi-identifiers, magari ptrebbe tornarci utile
'''
def guess_quasi_identifiers(df: pd.DataFrame) -> list:
    # Lista estesa e comune di parole chiave quasi-identificatori
    quasi_ids_keywords = {
        "age", "birthdate", "year_of_birth", "date_of_birth",
        "zipcode", "postal_code", "zip", "postcode",
        "city", "town", "municipality",
        "state", "province", "region",
        "gender", "sex",
        "race", "ethnicity",
        "marital_status", "maritalstatus",
        "occupation", "job_title", "profession",
        "education", "education_level", "degree",
        "phone_number", "telephone", "mobile",
        "email_domain", "email",
        "address", "street", "street_address",
        "country",
        "household_size", "family_size", "num_children",
        "nationality",
        "language",
        "birth_year", "birth_month", "birth_day",
    }
    
    quasi_identifiers = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Se il nome della colonna contiene una keyword nella lista
        if any(keyword in col_lower for keyword in quasi_ids_keywords):
            quasi_identifiers.append(col)
            continue
        
        # Controllo del tipo di dato e valori per riconoscere quasi-identificatori comuni
        # Esempio: se numerico e valori plausibili per età
        if pd.api.types.is_numeric_dtype(df[col]):
            values = df[col].dropna()
            if not values.empty:
                min_val, max_val = values.min(), values.max()
                # Età plausibile da 0 a 120 anni
                if 0 <= min_val <= 120 and 0 <= max_val <= 120:
                    quasi_identifiers.append(col)
                    continue
        
        # Codice postale spesso è stringa numerica corta
        if pd.api.types.is_string_dtype(df[col]):
            values = df[col].dropna().astype(str)
            # Se almeno il 90% delle stringhe sono numeri e lunghezza tra 4 e 7 -> probabile CAP
            num_count = sum(v.isdigit() and 4 <= len(v) <= 7 for v in values)
            if len(values) > 0 and (num_count / len(values)) >= 0.9:
                quasi_identifiers.append(col)
                continue
        
    return quasi_identifiers
    '''