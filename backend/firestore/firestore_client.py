from google.cloud import firestore
import logging

# Logging setup
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# Client singleton
def get_firestore_client():
    try:
        client = firestore.Client()
        logger.info("Firestore client created successfully")
        return client
    except Exception as e:
        logger.error(f"Error creating Firestore client: {e}")
        raise