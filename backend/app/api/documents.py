from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import parse_document
from app.utils.validation import validate_file_type
from app.utils.chunking import chunk_text
from app.core.embeddings import store_embeddings
import logging

router = APIRouter(prefix="/process-document", tags=["documents"])

@router.post("/")
async def process_document(file: UploadFile = File(...)):
    try:
        validate_file_type(file.filename)
        text = await parse_document(file)
        chunks = chunk_text(text)
        # Use document_id=1 for all documents (simplified for demo)
        store_embeddings(chunks, document_id=1)
        logging.info(f"Processed {file.filename}: {len(chunks)} chunks.")
        return {"chunks": len(chunks), "status": "processed"}
    except Exception as e:
        logging.error(f"Error processing document {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing document: {e}")