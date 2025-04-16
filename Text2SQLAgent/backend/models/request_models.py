# request_models.py
# backend/models/request_models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
