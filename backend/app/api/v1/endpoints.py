from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import QueryRequest, QueryResponse
import logging
import os
from io import BytesIO

# Import document processing services
try:
    from ...services.document_processor import parse_document_from_bytes
    from ...services.llm_service import query_llm
    SERVICES_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Services import failed: {e}")
    SERVICES_AVAILABLE = False

# Simple in-memory document storage for the session
document_store = {}
document_counter = 0

router = APIRouter(prefix="/hackrx", tags=["hackrx"])

@router.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "message": "HackRx 6.0 Backend is running",
        "real_processing": SERVICES_AVAILABLE,
        "document_count": len(document_store)
    }

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Real document processing with memory optimization"""
    global document_counter
    try:
        filename = file.filename or "unknown"
        
        if not SERVICES_AVAILABLE:
            # Fallback to demo mode if services aren't available
            return {
                "filename": filename,
                "text_preview": "Document uploaded successfully! Services temporarily unavailable - using demo mode.",
                "num_chunks": 5,
                "status": "success",
                "message": "File received and ready for querying",
                "document_id": 1
            }
        
        # Read file content
        content = await file.read()
        
        # Limit file size to avoid memory issues (2MB max)
        if len(content) > 2 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 2MB.")
        
        # Parse the document
        try:
            text_content = await parse_document_from_bytes(content, filename)
            
            # Limit text length to avoid memory issues
            if len(text_content) > 10000:
                text_content = text_content[:10000] + "... [truncated for memory optimization]"
            
            # Store the document
            document_counter += 1
            document_id = document_counter
            
            document_store[document_id] = {
                "filename": filename,
                "content": text_content,
                "size": len(content)
            }
            
            # Create preview
            preview = text_content[:300] + "..." if len(text_content) > 300 else text_content
            
            return {
                "filename": filename,
                "text_preview": preview,
                "num_chunks": len(text_content.split('\n')),
                "status": "success",
                "message": "Document processed successfully",
                "document_id": document_id,
                "content_length": len(text_content)
            }
            
        except Exception as parse_error:
            logging.error(f"Parsing error for {filename}: {parse_error}")
            raise HTTPException(status_code=400, detail=f"Could not parse document: {str(parse_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return {
            "error": f"Upload failed: {str(e)}",
            "filename": filename,
            "status": "error"
        }

@router.post("/run")
def run_query(payload: QueryRequest):
    """Real query processing with document context"""
    try:
        # Handle both single question and multiple questions
        questions = []
        if payload.questions:
            questions = [q for q in payload.questions if q and q.strip()]
        elif payload.question:
            questions = [payload.question]
        
        if not questions:
            questions = ["What is this document about?"]
        
        # Get document content if document_id is provided
        document_content = ""
        if payload.document_id and payload.document_id in document_store:
            doc = document_store[payload.document_id]
            document_content = doc["content"]
            document_filename = doc["filename"]
        else:
            document_filename = "uploaded document"
        
        # Generate responses for each question
        answers = []
        for i, question in enumerate(questions):
            if SERVICES_AVAILABLE and document_content and query_llm:
                try:
                    # Use real LLM to answer the question with document context
                    llm_response = query_llm(question, document_content)
                    
                    # Format the response nicely
                    formatted_response = f"""
🔍 Query: "{question}"

� Document: {document_filename}

�📋 Analysis Results:
✅ Document content analyzed
✅ Context-aware response generated using AI

💡 Answer:
{llm_response}

🎯 Information Source: Extracted from the uploaded document content
                    """
                    
                    answers.append({
                        "question": question,
                        "answer": formatted_response.strip(),
                        "confidence": 0.85
                    })
                    
                except Exception as llm_error:
                    logging.error(f"LLM error: {llm_error}")
                    # Fallback to basic text search
                    basic_answer = extract_relevant_text(document_content, question)
                    answers.append({
                        "question": question,
                        "answer": f"Based on document analysis: {basic_answer}",
                        "confidence": 0.70
                    })
            else:
                # Fallback response when LLM is not available
                if document_content:
                    basic_answer = extract_relevant_text(document_content, question)
                    fallback_response = f"""
🔍 Query: "{question}"

📄 Document: {document_filename}

📋 Basic Text Analysis:
{basic_answer}

💡 Note: This is a basic text extraction. Full AI analysis requires API keys.
                    """
                else:
                    fallback_response = f"""
🔍 Query: "{question}"

⚠️ No document found with ID: {payload.document_id}

💡 Please upload a document first, then try your query again.
                    """
                
                answers.append({
                    "question": question,
                    "answer": fallback_response.strip(),
                    "confidence": 0.60
                })
        
        # Return format that matches frontend expectations
        if len(answers) == 1 and payload.question:
            # Single question format
            return QueryResponse(result=answers[0]["answer"], confidence=answers[0]["confidence"])
        else:
            # Multiple questions format
            return {
                "answers": answers,
                "status": "success",
                "document_id": payload.document_id
            }
        
    except Exception as e:
        logging.error(f"Query processing error: {e}")
        return QueryResponse(
            result=f"Query processing failed: {str(e)}", 
            confidence=0.0
        )

def extract_relevant_text(content: str, question: str) -> str:
    """Basic text extraction based on keywords from question"""
    if not content:
        return "No document content available."
    
    # Simple keyword matching
    question_words = question.lower().split()
    keywords = [word for word in question_words if len(word) > 3]
    
    sentences = content.split('.')
    relevant_sentences = []
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in keywords):
            relevant_sentences.append(sentence.strip())
            if len(relevant_sentences) >= 3:  # Limit to 3 relevant sentences
                break
    
    if relevant_sentences:
        return ". ".join(relevant_sentences) + "."
    else:
        # Return first few sentences if no keywords match
        return ". ".join(sentences[:2]) + "." if len(sentences) >= 2 else content[:500] + "..."
