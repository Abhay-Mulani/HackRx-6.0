from pydantic import BaseModel
from typing import List, Union, Optional

class QueryRequest(BaseModel):
    document_id: Union[str, int]
    question: Optional[str] = None
    questions: Optional[List[str]] = None
 
class QueryResponse(BaseModel):
    result: str
    confidence: float 