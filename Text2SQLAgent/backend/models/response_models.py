# response_models.py
# backend/models/response_models.py
from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str
