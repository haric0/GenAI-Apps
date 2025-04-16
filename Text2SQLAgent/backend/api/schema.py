from fastapi import APIRouter, UploadFile, File, HTTPException
from services.vector_store import VectorStoreService
from utils.schema_parser import parse_schema_file
from core.logger import get_logger

router = APIRouter()
vector_service = VectorStoreService()
logger = get_logger(__name__)

@router.post("/update_schema")
async def update_schema(file: UploadFile = File(...)):
    logger.info("Calling the /update_schema endpoint")
    
    try:
        contents = await file.read()
        logger.info(f"Received file: {file.filename}, size: {len(contents)} bytes")

        schema_text = contents.decode("utf-8")
        parsed_schema = parse_schema_file(schema_text)
        logger.info(f"Parsed {len(parsed_schema)} schema chunks")

        # Get sample embedding size
        if parsed_schema:
            sample_embedding = vector_service.model.encode([parsed_schema[0]])
            logger.info(f"Embedding size: {len(sample_embedding[0])}")

        vector_service.reset_db()
        vector_service.store_schema(parsed_schema)
        logger.info("Schema stored successfully")

        return {"message": "Schema updated successfully."}

    except Exception as e:
        logger.error(f"Failed to update schema: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update schema: {str(e)}")
