import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get('MONGO_URL')

async def seed_academic_content():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['metrou_db']

    # 📚 استخراج شامل من مذكرة "Le Prince"
    full_curriculum = [
        {
            "id": "GR-001", "level": 1, "order": 1,
            "title": "الجملة الخبرية (La phrase)",
            "content": "تتكون من فاعل (Sujet)، فعل (Verbe)، ومفعول (Complément)[cite: 22].",
            "details": "الفاعل: قد يكون اسماً (Ahmed) أو ضميراً (Je, Tu, Il, Elle, Nous, Vous, Ils, Elles)[cite: 30, 36].",
            "examples": [{"fr": "Ezz El Din va au lycée", "ar": "عز الدين يذهب إلى المدرسة [cite: 74]"}]
        },
        {
            "id": "GR-002", "level": 1, "order": 2,
            "title": "تصنيف الأفعال (Les Verbes)",
            "content": "تنقسم الأفعال إلى 3 مجموعات حسب نهايتها[cite: 84].",
            "details": "المجموعة 1 تنتهي بـ er (parler)، المجموعة 2 تنتهي بـ ir (finir)، المجموعة 3 شاذة تنتهي بـ ir/re/oir (être, avoir)[cite: 85].",
            "examples": [{"fr": "parler / finir / être", "ar": "يتحدث / ينهي / يكون [cite: 85]"}]
        },
        {
            "id": "GR-003", "level": 1, "order": 3,
            "title": "فعل الكينونة (Être) - شاذ",
            "content": "أهم فعل شاذ في المجموعة الثالثة[cite: 85, 932].",
            "details": "Je suis, Tu es, Il/Elle est, Nous sommes, Vous êtes, Ils/Elles sont[cite: 932].",
            "examples": [{"fr": "Je suis étudiant", "ar": "أنا طالب [cite: 53]"}]
        },
        {
            "id": "GR-004", "level": 1, "order": 4,
            "title": "فعل الملكية (Avoir) - شاذ",
            "content": "يستخدم للتعبير عن الملكية والعمر[cite: 85, 933].",
            "details": "J'ai, Tu as, Il/Elle a, Nous avons, Vous avez, Ils/Elles ont[cite: 933].",
            "examples": [{"fr": "Il a 15 ans", "ar": "هو عنده 15 سنة [cite: 225]"}]
        },
        {
            "id": "GR-005", "level": 1, "order": 5,
            "title": "أدوات المعرفة (L'article défini)",
            "content": "تحدد نوع الاسم (مذكر/مؤنث) وعدده (مفرد/جمع)[cite: 100, 105].",
            "details": "Le (مذكر مفرد)، La (مؤنث مفرد)، L' (أمام حرف متحرك)، Les (للجمع بنوعيه)[cite: 110].",
            "examples": [{"fr": "Le livre / La table", "ar": "الكتاب / الطاولة [cite: 110]"}]
        }
    ]

    print("⏳ جاري تنظيف القاعدة وحقن المنهج الأكاديمي الشامل...")
    await db.lessons.delete_many({}) 
    await db.lessons.insert_many(full_curriculum)
    print(f"✅ تم بنجاح حقن {len(full_curriculum)} درساً أساسياً من المذكرة.")

if __name__ == "__main__":
    asyncio.run(seed_academic_content())
