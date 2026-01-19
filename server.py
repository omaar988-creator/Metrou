import os
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
import random

app = FastAPI()

# تفعيل الاتصال بين الموقع والسيرفر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعدادات قاعدة البيانات (تأكد من وجود MONGO_URL في Render)
MONGO_URL = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(MONGO_URL)
db = client['metrou_db']

class AIRequest(BaseModel):
    topic: str

@app.on_event("startup")
async def startup_event():
    # بذر البيانات تلقائياً إذا كانت فارغة
    if await db.lessons.count_documents({}) == 0:
        lessons = [
            {"id": "L1", "title": "الترحيب", "content": "Bonjour = مرحباً", "level": 1, "order": 1},
            {"id": "L2", "title": "الأرقام", "content": "Un, Deux, Trois", "level": 1, "order": 2},
            {"id": "L3", "title": "الأفعال", "content": "Être = يكون", "level": 1, "order": 3}
        ]
        await db.lessons.insert_many(lessons)
        print("✅ قاعدة البيانات جاهزة ومملوءة!")

@app.get("/api/lessons")
async def get_lessons():
    cursor = db.lessons.find({}, {"_id": 0})
    return await cursor.to_list(length=100)

@app.post("/api/ai/inspect")
async def ai_inspect(request: AIRequest):
    # نظام المفتش الذكي
    questions = [
        f"المفتش يوقفك! كيف تقول '{request.topic}' بالفرنسية؟",
        f"كمين مفاجئ! هل تتذكر درس '{request.topic}'؟ ترجم كلمة واحدة منه.",
        f"المفتش يطلب هويتك اللغوية: ما هو عكس كلمة 'Bonjour'؟"
    ]
    return {"question": random.choice(questions)}

@app.get("/")
async def root():
    return {"message": "سيرفر مترو يعمل بنجاح!"}
