from fastapi import APIRouter
from app.etl.ingestion_df import db_ingestion

router = APIRouter()

@router.post("/ingest")
def run_ingestion():
    db_ingestion()
    return {"message": "Ingestão realizada com sucesso"}
