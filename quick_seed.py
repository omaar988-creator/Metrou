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
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get('MONGO_URL')

async def seed_mega_content():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['metrou_db']

    # 1. مسح شامل ونهائي
    await db.lessons.delete_many({})
    await db.vocabulary.delete_many({})
    await db.quizzes.delete_many({})

    # 🏛️ 2. المنهج الأكاديمي الشامل (مستخلص من مذكرة Le Prince)
    academic_lessons = [
        {"id": "GR-001", "level": 1, "order": 1, "title": "مكونات الجملة الفرنسية", "content": "تتكون الجملة الخبرية من فاعل (Sujet)، فعل (Verbe)، ومفعول (Complément). [cite: 19]", "details": "الفاعل ينقسم إلى اسم (Nom) أو ضمير (Pronom) مثل Je, Tu. [cite: 27, 33]", "examples": [{"fr": "Ezz El Din va au lycée", "ar": "عز الدين يذهب للمدرسة الثانوية. [cite: 74]"}]},
        {"id": "GR-002", "level": 1, "order": 2, "title": "مجموعات الأفعال الثلاث", "content": "تنقسم الأفعال حسب نهايتها: مجموعة 1 (er)، مجموعة 2 (ir)، مجموعة 3 (ir/re/oir). [cite: 84, 85]", "details": "أفعال المجموعة الأولى هي الأكثر شيوعاً. [cite: 749]", "examples": [{"fr": "Parler (يتحدث)", "ar": "مجموعة أولى. [cite: 85]"}]},
        {"id": "GR-003", "level": 1, "order": 3, "title": "أدوات المعرفة والنكرة", "content": "تستخدم لتحديد نوع الاسم وعدده. [cite: 100]", "details": "النكرة: un, une, des. [cite: 103] المعرفة: le, la, l', les. [cite: 109]", "examples": [{"fr": "Un garçon / La table", "ar": "ولد / الطاولة. [cite: 103, 110]"}]},
        {"id": "GR-004", "level": 1, "order": 4, "title": "فعل الكينونة والملكية", "content": "أهم فعلين في اللغة: Être (يكون) و Avoir (يملك). [cite: 932, 933]", "details": "تصريف Être: Je suis, Tu es.. [cite: 932] وتصريف Avoir: J'ai, Tu as.. [cite: 941]", "examples": [{"fr": "Je suis étudiant", "ar": "أنا طالب. [cite: 49]"}]}
    ]

    # 📜 3. الموسوعة الثقافية (تاريخ، سياسة، مرأة، شارع، حكم)
    cultural_hub = [
        # تاريخ وسياسة
        {"category": "history", "title": "الثورة الفرنسية 1789", "content": "قامت للقضاء على الاستبداد ورفعت شعار الحرية والمساواة والإخاء.", "type": "official"},
        {"category": "politics", "author": "Charles de Gaulle", "quote": "Paris outragé! Paris brisé! Paris martyrisé! Mais Paris libéré!", "ar": "باريس أُهينت! كُسرت! عُذبت! ولكنها حُررت!", "type": "official"},
        # نضال المرأة (سيمون دي بوفوار)
        {"category": "women_rights", "figure": "Simone de Beauvoir", "content": "كاتبة ومفكرة فرنسية دافعت عن حقوق المرأة، صاحبة كتاب 'الجنس الآخر'.", "type": "official"},
        {"category": "women_rights", "figure": "حق التصويت", "content": "حصلت المرأة الفرنسية على حق التصويت في عام 1944.", "type": "official"},
        # لغة الشارع (Argot & Verlan)
        {"category": "street_line", "fr": "Cimer", "standard": "Merci", "ar": "شكراً (بلغة الشارع بقلب الكلمة).", "type": "slang"},
        {"category": "street_line", "fr": "Ouf", "standard": "Fou", "ar": "مجنون / رائع جداً.", "type": "slang"},
        {"category": "street_line", "fr": "Meuf", "standard": "Femme", "ar": "امرأة / فتاة.", "type": "slang"},
        # حكم وأمثال
        {"category": "proverbs", "fr": "Petit à petit, l'oiseau fait son nid", "ar": "قطرة قطرة يصنع الطائر عشه (في التأني السلامة).", "type": "proverb"}
    ]

    # ✍️ 4. تمارين المهارات الأربع (كتابة، قراءة، استماع، تحدث)
    quizzes = [
        {"id": "Q_WRITE_1", "lesson_id": "GR-001", "type": "writing", "question": "اكتب بالفرنسية: أنا أكون مدرساً", "correct": "Je veux être professeur", "explanation": "استخدام فعل الكينونة في المصدر بعد فعل مصرف. [cite: 921]"},
        {"id": "Q_CHOICE_1", "lesson_id": "GR-003", "type": "choice", "question": "C'est ...... petit garçon. [cite: 177]", "options": ["un", "une", "des"], "correct": "un", "explanation": "garçon مذكر مفرد. [cite: 179]"}
    ]

    # التنفيذ الفوري
    print("⏳ جاري تنظيف وحقن 'مترو الموسوعة الشاملة'...")
    await db.lessons.insert_many(academic_lessons)
    await db.vocabulary.insert_many(cultural_hub)
    await db.quizzes.insert_many(quizzes)
    print(f"✅ تم الضخ: {len(academic_lessons)} دروس، {len(cultural_hub)} محطات ثقافية، {len(quizzes)} تمارين.")

if __name__ == "__main__":
    asyncio.run(seed_mega_content())
