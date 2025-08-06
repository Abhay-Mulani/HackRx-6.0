from pydantic import BaseModel

class QueryRequest(BaseModel):
    document_id: str
    question: str
 
class QueryResponse(BaseModel):
    result: str
    confidence: float 