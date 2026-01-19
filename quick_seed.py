import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# تأكد من أن MONGO_URL مضاف في إعدادات Render
MONGO_URL = os.environ.get('MONGO_URL')

async def seed_academic_content():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['metrou_db']

    # --- 1. عينة من دروس القواعد الاحترافية (Grammar) ---
    grammar_lessons = [
        {
            "id": "GR-001",
            "level": "A1",
            "title": "أدوات التعريف (Les Articles Définis)",
            "content": "تُستخدم أدوات التعريف لتحديد اسم معين معروف لدى المتحدث والمستمع.",
            "rule": "Le (للمذكر)، La (للمؤنث)، L' (للمفرد المبدوء بحرف علة)، Les (للجمع).",
            "examples": [
                {"fr": "Le livre est sur la table", "ar": "الكتاب على الطاولة"},
                {"fr": "L'école هي المدرسة", "ar": "المدرسة"}
            ],
            "order": 1
        },
        {
            "id": "GR-002",
            "level": "A1",
            "title": "فعل الكينونة (Verbe Être) في المضارع",
            "content": "يعتبر أهم فعل في اللغة الفرنسية، ويستخدم للتعريف عن النفس، المهنة، أو الحالة.",
            "rule": "Je suis, Tu es, Il/Elle est, Nous sommes, Vous êtes, Ils/Elles sont.",
            "examples": [
                {"fr": "Je suis étudiant", "ar": "أنا طالب"},
                {"fr": "Nous sommes heureux", "ar": "نحن سعداء"}
            ],
            "order": 2
        }
    ]

    # --- 2. عينة من بنك الجمل (Sentence Bank) ---
    sentences_bank = [
        {"fr": "Comment puis-je vous aider ?", "ar": "كيف يمكنني مساعدتك؟", "category": "General"},
        {"fr": "C'est un plaisir de vous rencontrer", "ar": "إنه لمن دواعي سروري لقاؤك", "category": "Social"},
        {"fr": "Pouvez-vous répéter سيل فوبليه ؟", "ar": "هل يمكنك التكرار من فضلك؟", "category": "Learning"}
    ]

    # التنفيذ: مسح القديم وحقن الجديد
    print("⏳ جاري تنظيف وحقن المحتوى الأكاديمي...")
    await db.lessons.delete_many({}) # نمسح العينات القديمة البسيطة
    await db.lessons.insert_many(grammar_lessons)
    
    if await db.vocabulary.count_documents({}) == 0:
        await db.vocabulary.insert_many(sentences_bank)
        
    print(f"✅ تم حقن {len(grammar_lessons)} دروس قواعد و {len(sentences_bank)} جمل.")

if __name__ == "__main__":
    asyncio.run(seed_academic_content())
