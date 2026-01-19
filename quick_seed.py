import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get('MONGO_URL')

async def reset_and_seed():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['metrou_db']
    
    # مسح شامل للداتا القديمة
    await db.lessons.delete_many({})
    await db.vocabulary.delete_many({})
    await db.quizzes.delete_many({})

    # 🏛️ 1. المنهج الأكاديمي (Le Prince)
    academic = [
        {"id": "GR-001", "level": 1, "order": 1, "title": "الجملة الخبرية", "content": "تتكون من فاعل، فعل، ومفعول [cite: 18, 22].", "details": "الفاعل قد يكون اسماً أو ضميراً (Je, Tu, Il) [cite: 27, 33].", "examples": [{"fr": "Ali va au lycée", "ar": "علي يذهب للمدرسة[cite: 74]."}]},
        {"id": "GR-002", "level": 1, "order": 2, "title": "أدوات المعرفة", "content": "Le, La, L', Les [cite: 109, 111].", "details": "تستخدم لتعريف الاسم وتحديد نوعه [cite: 110].", "examples": [{"fr": "Le livre", "ar": "الكتاب[cite: 110]."}]}
    ]

    # 📜 2. الخطوط الثقافية والشارع
    cultural = [
        {"category": "history", "title": "الثورة الفرنسية", "content": "حدثت عام 1789 وغيرت وجه العالم شعارها (Liberté, Égalité, Fraternité).", "type": "official"},
        {"category": "politics", "author": "Charles de Gaulle", "quote": "Paris libéré!", "ar": "باريس حُررت!", "type": "official"},
        {"category": "women_rights", "figure": "Simone de Beauvoir", "content": "رائدة نضال المرأة الفرنسية وحقوقها السياسية[cite: 22].", "type": "official"},
        {"category": "street_line", "fr": "Cimer", "standard": "Merci", "ar": "شكراً (بلغة الشارع)", "type": "slang"},
        {"category": "proverbs", "fr": "C'est la vie", "ar": "هذه هي الحياة", "type": "common"}
    ]

    await db.lessons.insert_many(academic)
    await db.vocabulary.insert_many(cultural)
    print("✅ تم مسح الداتا القديمة وضخ 5 خطوط مترو جديدة بنجاح!")

if __name__ == "__main__":
    asyncio.run(reset_and_seed())
