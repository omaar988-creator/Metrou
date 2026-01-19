from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import httpx

# 1. إعداد البيئة
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME', 'metrou_db')

if not MONGO_URL:
    print("Warning: MONGO_URL not found")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# ============== MODELS ==============

class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    native_language: str = "ar"
    created_at: datetime
    daily_streak: int = 0
    total_points: int = 0
    is_premium: bool = False
    premium_expires: Optional[datetime] = None
    energy: int = 5

class UserSession(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

class SessionDataResponse(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    session_token: str

class AIExplainRequest(BaseModel):
    topic: str
    user_language: str = "ar"

class AIQuizRequest(BaseModel):
    topic: str
    difficulty: int = 1
    count: int = 5

class ConsumeEnergyRequest(BaseModel):
    amount: int = 1

# ============== UTILITIES ==============

async def get_current_user(request: Request) -> Optional[User]:
    session_token = request.cookies.get("session_token")
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.replace("Bearer ", "")
    
    if not session_token:
        return None
    
    session = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if not session:
        return None
    
    expires_at = session["expires_at"]
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    
    user_doc = await db.users.find_one({"user_id": session["user_id"]}, {"_id": 0})
    if user_doc:
        return User(**user_doc)
    return None

# ============== API ENDPOINTS ==============

@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Metrou Backend is running!"}

@api_router.post("/auth/exchange-session")
async def exchange_session(request: Request, response: Response):
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")
    
    # محاكاة تسجيل الدخول (سيتم ربطها لاحقاً)
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    session_token = str(uuid.uuid4())
    
    return SessionDataResponse(
        id=user_id,
        email="test@example.com",
        name="Test User",
        picture="",
        session_token=session_token
    )

@api_router.get("/grammar/lessons")
async def get_grammar_lessons(category: Optional[str] = None):
    query = {}
    if category:
        query["category"] = category
    lessons = await db.grammar_lessons.find(query, {"_id": 0}).sort("order", 1).to_list(100)
    return lessons

@api_router.get("/vocabulary/words")
async def get_vocabulary(category: Optional[str] = None, limit: int = 50):
    query = {}
    if category:
        query["category"] = category
    words = await db.vocabulary.find(query, {"_id": 0}).limit(limit).to_list(None)
    return words

@api_router.get("/sentences")
async def get_sentences(difficulty: Optional[int] = None, limit: int = 50):
    query = {}
    if difficulty:
        query["difficulty"] = difficulty
    sentences = await db.sentences.find(query, {"_id": 0}).limit(limit).to_list(None)
    return sentences

# --- AI Endpoints (Temporary Placeholder) ---
@api_router.post("/ai/explain")
async def ai_explain(data: AIExplainRequest, request: Request):
    return {"explanation": "خدمة الذكاء الاصطناعي ستتوفر قريباً!"}

@api_router.post("/ai/quiz")
async def ai_quiz(data: AIQuizRequest, request: Request):
    return {"quiz": []}

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
