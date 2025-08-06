import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import only the minimal API routes
from app.api.v1.endpoints import router as hackrx_router

app = FastAPI(title="HackRx 6.0 Query Retrieval System - Lightweight")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include only the essential router
app.include_router(hackrx_router)

@app.get("/")
def read_root():
    return {"message": "HackRx 6.0 API is running", "status": "healthy"} 