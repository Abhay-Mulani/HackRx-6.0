from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.core.embeddings import search_similar_chunks
from app.services.llm import ask_llm
import logging

router = APIRouter(prefix="/ask-question", tags=["queries"])

class QueryRequest(BaseModel):
    question: str
    document_id: int

class MultipleQueryRequest(BaseModel):
    questions: List[str]
    document_id: int

@router.post("/")
async def ask_question(req: QueryRequest):
    context_chunks = search_similar_chunks(req.document_id, req.question)
    answer = ask_llm(req.question, context_chunks)
    logging.info(f"Answered question: {req.question[:50]}...")
    logging.info(f"Full answer: {answer}")
    return {"answer": answer, "sources": context_chunks}

@router.post("/multiple")
async def ask_multiple_questions(req: MultipleQueryRequest):
    results = []
    for question in req.questions:
        context_chunks = search_similar_chunks(req.document_id, question)
        answer = ask_llm(question, context_chunks)
        results.append(answer)
        logging.info(f"Answered question: {question[:50]}...")
        logging.info(f"Full answer: {answer}")
    
    return {"answers": results} 