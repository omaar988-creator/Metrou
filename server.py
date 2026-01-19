import os
import google.generativeai as genai
from fastapi import FastAPI, APIRouter, HTTPException
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Dict, Optional

# 1. إعداد البيئة والذكاء الاصطناعي
# سيقوم السيرفر بجلب المفتاح تلقائياً من إعدادات Render التي شرحناها
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
MONGO_URL = os.environ.get('MONGO_URL')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

# تفعيل الوصول من موقعك على GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# ============== نماذج البيانات ==============
class AIExplainRequest(BaseModel):
    topic: str

class UserUpdate(BaseModel):
    name: str

# ============== نقاط اتصال التطبيق (Endpoints) ==============

# 1. نظام محطات المترو لتعلم الفرنسية
@api_router.get("/metro/map")
async def get_metro_map():
    stations = [
        {"id": 1, "name_ar": "الترحيب", "name_fr": "Salutations", "status": "open"},
        {"id": 2, "name_ar": "الأفعال الأساسية", "name_fr": "Verbes de base", "status": "locked"},
        {"id": 3, "name_ar": "أدوات التعريف", "name_fr": "Les Articles", "status": "locked"}
    ]
    return stations

# 2. ربط Gemini لشرح القواعد
@api_router.post("/ai/explain")
async def ai_explain(data: AIExplainRequest):
    try:
        prompt = f"أنت معلم لغة فرنسية خبير. اشرح موضوع '{data.topic}' باللغة العربية بأسلوب مبسط جداً مع 3 أمثلة فرنسية وترجمتها."
        response = ai_model.generate_content(prompt)
        return {"explanation": response.text}
    except Exception as e:
        return {"explanation": "يرجى التأكد من تفعيل مفتاح Gemini في إعدادات السيرفر."}

# 3. تحديث اسم المستخدم
@api_router.post("/user/update-name")
async def update_name(data: UserUpdate):
    return {"message": f"أهلاً بك يا {data.name} في تطبيق Metrou"}

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# نموذج طلب التفتيش
class InspectionRequest(BaseModel):
    past_topics: List[str]

@api_router.post("/ai/inspect")
async def ai_inspect(data: InspectionRequest):
    try:
        topics = ", ".join(data.past_topics)
        prompt = f"""
        أنت الآن 'مفتش مترو اللغة الفرنسية'. 
        قم باختيار سؤال واحد عشوائي من المواضيع التالية: {topics}.
        يجب أن يكون السؤال قصيراً (اختيار من متعدد).
        إذا أخطأ المستخدم، اقترح عليه عقاباً طريفاً (مثلاً: تنظيف زجاج المترو، أو الغناء بالفرنسية في المحطة).
        تحدث بلهجة المفتش الحازم ولكن الفكاهي.
        """
        response = ai_model.generate_content(prompt)
        return {"inspection_query": response.text}
    except Exception as e:
        return {"inspection_query": "المفتش مشغول الآن، يمكنك المرور!"}
# في ملف server.py

@api_router.post("/api/metro/request-passage")
async def request_passage(data: Dict[str, str]):
    current_station = data.get("from_station", "التحيات")
    
    # اطلب من جيميناي توليد سؤال تفتيش سريع (مراجعة)
    prompt = f"أنت مفتش مترو اللغة الفرنسية. المستخدم يريد الانتقال من محطة {current_station}. اطرح عليه سؤالاً واحداً (اختيارات) مراجعة لما تعلمه، وإذا فشل، قل له عقاباً فكاهياً."
    
    try:
        response = ai_model.generate_content(prompt)
        return {"inspection_question": response.text}
    except:
        return {"inspection_question": "أين تذكرتك؟ قل 'Bonjour' لتمر!"}
