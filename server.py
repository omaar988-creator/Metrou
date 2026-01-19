from fastapi import FastAPI, APIRouter, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

# 1. إعداد البيئة والذكاء الاصطناعي
MONGO_URL = os.environ.get('MONGO_URL')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

client = AsyncIOMotorClient(MONGO_URL)
db = client['metrou_db']

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

api_router = APIRouter(prefix="/api")

# ============== MODELS ==============
class AIExplainRequest(BaseModel):
    topic: str
    user_language: str = "ar"

class UserUpdate(BaseModel):
    name: str

# ============== API ENDPOINTS ==============

# 1. نظام محطات المترو (تطوير المحطة)
@api_router.get("/metro/map")
async def get_metro_map():
    # تم تحديث المحطات لتناسب تعلم الفرنسية
    stations = [
        {"id": 1, "name_ar": "بداية الرحلة", "name_fr": "Le Départ", "topic": "Les Salutations", "status": "open"},
        {"id": 2, "name_ar": "محطة الأفعال", "name_fr": "Les Verbes", "topic": "Être et Avoir", "status": "locked"},
        {"id": 3, "name_ar": "محطة القواعد", "name_fr": "La Grammaire", "topic": "Le Genre", "status": "locked"}
    ]
    return stations

# 2. ربط Gemini لشرح القواعد الفرنسية
@api_router.post("/ai/explain")
async def ai_explain(data: AIExplainRequest):
    try:
        prompt = f"أنت معلم لغة فرنسية خبير. اشرح موضوع '{data.topic}' باللغة العربية بأسلوب مبسط مع أمثلة فرنسية مترجمة."
        response = ai_model.generate_content(prompt)
        return {"explanation": response.text}
    except Exception as e:
        return {"explanation": "حدث خطأ في الاتصال بـ Gemini، يرجى التأكد من مفتاح API."}

# 3. تغيير اسم المستخدم (Profile)
@api_router.post("/user/update-name")
async def update_name(data: UserUpdate):
    # هنا يتم التعديل في MongoDB لاحقاً
    return {"message": f"تم تغيير اسمك إلى: {data.name}"}

app.include_router(api_router)

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
