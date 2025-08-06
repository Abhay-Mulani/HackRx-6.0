from pydantic import BaseModel
from typing import List, Union, Optional

class QueryRequest(BaseModel):
    documents: str  # URL to document or document identifier
    questions: List[str]  # Array of questions as per HackRx format

class QueryResponse(BaseModel):
    answers: List[str]  # Simple array of answers as per HackRx format 