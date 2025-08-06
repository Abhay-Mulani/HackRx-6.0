from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from core.security import (
    get_api_key, get_password_hash, authenticate_user, create_access_token, User, UserIn, fake_users_db, get_current_user
)
from .schemas import QueryRequest, QueryResponse
from core.security import something
from services.vector_db import search_vectors
from services.llm_service import query_llm
from utils.document_parser import parse_document
from utils.chunking import chunk_text
from datetime import timedelta

router = APIRouter(prefix="/hackrx", tags=["hackrx"])

@router.post("/run", response_model=QueryResponse, dependencies=[Depends(get_api_key)])
def run_query(payload: QueryRequest):
    doc = parse_document(payload.document_id)
    chunks = chunk_text(doc["text"])
    docs = search_vectors(payload.question)
    result = query_llm(payload.question, context=doc["text"])
    return QueryResponse(result=result, confidence=0.95)

@router.post("/upload", dependencies=[Depends(get_api_key)])
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    doc = parse_document(file_path)
    chunks = chunk_text(doc["text"])
    return {"filename": file.filename, "text_preview": doc["text"][:200], "num_chunks": len(chunks)}

# --- Auth Endpoints ---
@router.post("/auth/register")
def register(user: UserIn):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    fake_users_db[user.username] = User(username=user.username, hashed_password=hashed)
    return {"msg": "User registered"}

@router.post("/auth/token")
def login(form_data: UserIn):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}

# --- Admin Analytics ---
@router.get("/admin/analytics", dependencies=[Depends(get_api_key)])
def admin_analytics():
    # Placeholder: return fake leaderboard and stats
    leaderboard = [
        {"team": "Alpha", "score": 120},
        {"team": "Bravo", "score": 110},
        {"team": "Charlie", "score": 90},
    ]
    stats = {"total_submissions": 42, "avg_accuracy": 0.91, "avg_speed": 1.2, "avg_efficiency": 0.88}
    return {"leaderboard": leaderboard, "stats": stats} 