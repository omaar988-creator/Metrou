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
# استيراد مكتبة الذكاء الاصطناعي
from emergentintegrations.llm.chat import LlmChat, UserMessage

# 1. إعداد البيئة
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# 2. إعداد الاتصال بقاعدة البيانات
# نستخدم os.environ.get لمنع حدوث خطأ إذا لم يجد المتغير فوراً
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME', 'metrou_db')

if not MONGO_URL:
    print("Warning: MONGO_URL not found in environment variables")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# 3. إنشاء التطبيق
app = FastAPI()

# إعداد CORS (مهم جداً ليعمل مع تطبيق الهاتف)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يسمح بالاتصال من أي مكان (للتطوير)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# ============== MODELS (نماذج البيانات) ==============

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
