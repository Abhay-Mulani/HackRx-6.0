from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import requests
import tempfile
import os
from app.services.document_processor import parse_document_from_bytes
from app.utils.chunking import chunk_text
from app.core.embeddings import store_embeddings, search_similar_chunks
from app.services.llm import ask_llm
import logging

router = APIRouter(prefix="/hackrx", tags=["hackrx"])
security = HTTPBearer()

class HackRxRequest(BaseModel):
    documents: str  # URL to the document
    questions: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple token verification - in production, implement proper JWT validation"""
    expected_token = "bc74b11a4fc4ff0cae1ed55777bfd110f31260057db07f14d6efd466b8536ea7"
    if credentials.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

@router.post("/run", response_model=HackRxResponse)
async def hackrx_run(request: HackRxRequest, token: str = Depends(verify_token)):
    """
    HackRx endpoint that processes a document from URL and answers multiple questions
    """
    try:
        # Download document from URL
        logging.info(f"Downloading document from: {request.documents}")
        doc_response = requests.get(request.documents)
        doc_response.raise_for_status()
        
        # Create a temporary file to mimic UploadFile behavior
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(doc_response.content)
            temp_file_path = temp_file.name
        
        try:
            # Parse the document
            logging.info("Parsing document...")
            text = await parse_document_from_bytes(doc_response.content, "policy.pdf")
            
            # Chunk the text
            chunks = chunk_text(text)
            logging.info(f"Created {len(chunks)} chunks")
            
            # Store embeddings with a unique document_id
            document_id = hash(request.documents) % 1000000  # Simple hash-based ID
            store_embeddings(chunks, document_id=document_id)
            logging.info(f"Stored embeddings for document_id: {document_id}")
            
            # Process each question
            answers = []
            for question in request.questions:
                logging.info(f"Processing question: {question[:50]}...")
                
                # Search for relevant chunks
                context_chunks = search_similar_chunks(document_id, question)
                
                # Get answer from LLM
                answer = ask_llm(question, context_chunks)
                answers.append(answer)
                
                logging.info(f"Answer: {answer[:100]}...")
            
            return HackRxResponse(answers=answers)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except requests.RequestException as e:
        logging.error(f"Error downloading document: {e}")
        raise HTTPException(status_code=400, detail=f"Error downloading document: {e}")
    except Exception as e:
        logging.error(f"Error processing HackRx request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")
