import os
from dotenv import load_dotenv, find_dotenv
# Load environment variables from .env file in backend directory
load_dotenv(find_dotenv())
import asyncio
import logging
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from app.api import documents, queries, hackrx

# Configure logging for explainability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from app.core.config import settings  # Import settings to access environment variables
# Debug log to verify GEMINI_API_KEY is loaded
logger.info(f"GEMINI_API_KEY loaded: {settings.GEMINI_API_KEY is not None}")

load_dotenv()

app = FastAPI(title="HackRx 6.0 Query Retrieval System")
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(queries.router)
app.include_router(hackrx.router) 