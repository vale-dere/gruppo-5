from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.cloud import firestore
from firestore.firestore_client import get_firestore_client  # suppongo che hai questa funzione
from auth.firebase_auth import verify_token  # importa il tuo verify_token
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn")

class DatasetMetadata(BaseModel):
    dataset_name: str
    description: str = None
    author: str = None

@router.post("/save-metadata")
async def save_metadata(
    data: DatasetMetadata,
    decoded_token=Depends(verify_token)  # usa la tua dipendenza per validare il token
):
    client = get_firestore_client()
    try:
        doc_ref = client.collection("datasets").document()
        doc_ref.set(data.dict())
        logger.info(f"Saved metadata for dataset: {data.dataset_name} by user {decoded_token['uid']}")
        return {"message": "Saved", "id": doc_ref.id}
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")
        raise HTTPException(status_code=500, detail="Firestore error")
