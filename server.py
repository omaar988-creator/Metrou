import os
from fastapi import FastAPI, Body, Query
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MONGO_URL = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(MONGO_URL)
db = client['metrou_db']

@app.get("/")
async def root():
    return {"message": "سيرفر مترو الموسوعي يعمل بنجاح! 🚇"}

@app.get("/api/lessons")
async def get_lessons():
    # جلب دروس المنهج الأكاديمي (Le Prince)
    cursor = db.lessons.find({}, {"_id": 0}).sort("order", 1)
    return await cursor.to_list(length=100)

@app.get("/api/encyclopedia")
async def get_content(category: str = Query(...)):
    # جلب محتوى الخطوط (تاريخ، سياسة، مرأة، شارع، حكم)
    cursor = db.vocabulary.find({"category": category}, {"_id": 0})
    return await cursor.to_list(length=100)

@app.post("/api/quiz/complete")
async def complete_quiz(data: dict = Body(...)):
    # نظام ترقية المستويات التخيلي (يمكن تطويره لربطه بحساب مستخدم)
    return {"status": "success", "message": "تم تحديث التقدم!"}
