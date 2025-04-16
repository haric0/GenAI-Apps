from fastapi import APIRouter
from pydantic import BaseModel
from core.logger import get_logger
import datetime
import time
from core.faiss_handler import VectorStore
from services.vector_store import VectorStoreService
from sentence_transformers import SentenceTransformer
import requests

router = APIRouter()
logger = get_logger(__name__)


vector_service = VectorStoreService()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()

    logger.info(f"[{timestamp}] Received query: {request.query}")
    
    try:
        query = request.query
        token_count = len(query.split())
        logger.info(f"Token count: {token_count}")

        # Step 1: Vector search
        results = vector_service.query(query, top_k=3)
        logger.info(f"Vector search results: {results}")

        if not results:
            logger.warning("No relevant tables found in vector DB.")
            return ChatResponse(response="No relevant tables found.")

        # Step 2: Build prompt using raw results
        prompt = (
            "You are an expert SQL generator. Based on the table schema definitions that exist in the database, identify the relevant table for query and provide an accurate SQL query:\n\n"
            + "\n\n".join(results) +
            "\n\nWrite an accurate SQL query for the user request:\n"
            + query
        )

        logger.debug(f"Prompt sent to LLM:\n{prompt}")

        # Step 3: Send to Ollama LLM
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            raise Exception(f"LLM error: {response.text}")

        llm_result = response.json().get("response", "").strip()
        logger.info(f"Generated SQL: {llm_result}")

        # Step 4: Logging and timing
        elapsed_time = time.time() - start_time
        logger.info(f"Response time: {elapsed_time:.4f} seconds")

        return ChatResponse(response=llm_result)

    except Exception as e:
        logger.error("Error during chat processing", exc_info=True)
        return ChatResponse(response="An error occurred while processing the query.")
