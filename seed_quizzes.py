import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get('MONGO_URL')

async def seed_quizzes():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['metrou_db']

    # تمارين مستخرجة من صفحة 5 و 13 في مذكرة "Le Prince"
    quizzes = [
        {
            "id": "Q1",
            "lesson_id": "GR-005",
            "question": "C'est ...... petit garçon.",
            "options": ["un", "une", "des"],
            "correct": "un",
            "explanation": "garçon اسم مفرد مذكر لذا نستخدم أداة النكرة un."
        },
        {
            "id": "Q2",
            "lesson_id": "GR-005",
            "question": "Ezz El Din a ...... grande sœur.",
            "options": ["un", "une", "des"],
            "correct": "une",
            "explanation": "sœur اسم مفرد مؤنث لذا نستخدم أداة النكرة une."
        },
        {
            "id": "Q3",
            "lesson_id": "GR-005",
            "question": "Salma a ...... nouvelle amie.",
            "options": ["un", "une", "des"],
            "correct": "une",
            "explanation": "amie اسم مفرد مؤنث."
        },
        {
            "id": "Q4",
            "lesson_id": "GR-003",
            "question": "Martine et Jean sont ......",
            "options": ["français", "française", "françaises"],
            "correct": "français",
            "explanation": "الجمع المذكر يغلب في اللغة الفرنسية عند اجتماع المذكر والمؤنث."
        },
        {
            "id": "Q5",
            "lesson_id": "GR-003",
            "question": "Tout le monde ...... le sport.",
            "options": ["aime", "aimes", "aiment"],
            "correct": "aime",
            "explanation": "تعبير Tout le monde يعامل معاملة المفرد (il)."
        }
    ]

    print("⏳ جاري شحن الاختبارات التفاعلية من المذكرة...")
    await db.quizzes.delete_many({}) 
    await db.quizzes.insert_many(quizzes)
    print(f"✅ تم بنجاح حقن {len(quizzes)} اختباراً تفاعلياً.")

if __name__ == "__main__":
    asyncio.run(seed_quizzes())
