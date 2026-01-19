import asyncio
import os
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# تحميل المتغيرات (مهم للتجربة المحلية، وفي Render يعمل تلقائياً)
load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME', 'metrou_db')

async def seed():
    if not MONGO_URL:
        print("❌ Error: MONGO_URL is missing!")
        return

    print(f'⏳ Connecting to Cloud DB...')
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    # --- 1. Grammar Lessons (دروس القواعد) ---
    lessons = [
        {
            'lesson_id': f'lesson_{uuid.uuid4().hex[:12]}',
            'category': 'pronunciation',
            'title': 'French Vowels',
            'title_ar': 'حروف العلة الفرنسية',
            'content': 'Learn the pronunciation of French vowels: a, e, i, o, u',
            'content_ar': 'تعلم نطق حروف العلة الفرنسية: a, e, i, o, u',
            'examples': ['chat (cat)', 'été (summer)', 'lit (bed)', 'mot (word)', 'rue (street)'],
            'level': 1, 'order': 1, 'created_at': datetime.now(timezone.utc)
        },
        {
            'lesson_id': f'lesson_{uuid.uuid4().hex[:12]}',
            'category': 'basic_grammar',
            'title': 'Articles (le, la, les)',
            'title_ar': 'أدوات التعريف',
            'content': 'French nouns have gender: masculine (le) or feminine (la)',
            'content_ar': 'الأسماء الفرنسية لها جنس: مذكر (le) أو مؤنث (la)',
            'examples': ['le chat (the cat)', 'la maison (the house)', 'les chats (the cats)'],
            'level': 1, 'order': 2, 'created_at': datetime.now(timezone.utc)
        }
    ]

    # --- 2. Vocabulary (الكلمات) ---
    vocab = [
        {'word_id': f'word_{uuid.uuid4().hex[:12]}', 'french_word': 'Bonjour', 'english_translation': 'Hello', 'arabic_translation': 'مرحباً', 'category': 'group1', 'example_sentence': 'Bonjour, ça va?', 'example_sentence_ar': 'مرحباً، كيف الحال؟', 'pronunciation': 'bon-zhour', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)},
        {'word_id': f'word_{uuid.uuid4().hex[:12]}', 'french_word': 'Merci', 'english_translation': 'Thank you', 'arabic_translation': 'شكراً', 'category': 'group1', 'example_sentence': 'Merci beaucoup', 'example_sentence_ar': 'شكراً جزيلاً', 'pronunciation': 'mer-see', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)},
        {'word_id': f'word_{uuid.uuid4().hex[:12]}', 'french_word': 'Oui', 'english_translation': 'Yes', 'arabic_translation': 'نعم', 'category': 'group1', 'example_sentence': 'Oui, c\'est ça', 'example_sentence_ar': 'نعم، هذا صحيح', 'pronunciation': 'wee', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)},
        {'word_id': f'word_{uuid.uuid4().hex[:12]}', 'french_word': 'Non', 'english_translation': 'No', 'arabic_translation': 'لا', 'category': 'group1', 'example_sentence': 'Non, merci', 'example_sentence_ar': 'لا، شكراً', 'pronunciation': 'noh', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)}
    ]

    # --- 3. Sentences (الجمل) ---
    sentences = [
        {'sentence_id': f'sent_{uuid.uuid4().hex[:12]}', 'french_text': 'Je voudrais un café', 'english_translation': 'I would like a coffee', 'arabic_translation': 'أريد قهوة', 'context': 'Restaurant', 'context_ar': 'في المقهى', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)},
        {'sentence_id': f'sent_{uuid.uuid4().hex[:12]}', 'french_text': 'Où est la gare?', 'english_translation': 'Where is the station?', 'arabic_translation': 'أين المحطة؟', 'context': 'Travel', 'context_ar': 'السفر', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)},
        {'sentence_id': f'sent_{uuid.uuid4().hex[:12]}', 'french_text': 'Parlez-vous anglais?', 'english_translation': 'Do you speak English?', 'arabic_translation': 'هل تتحدث الإنجليزية؟', 'context': 'General', 'context_ar': 'عام', 'difficulty': 1, 'created_at': datetime.now(timezone.utc)}
    ]

    # --- التنفيذ (الإدخال في القاعدة) ---
    print('🚀 Inserting Data...')
    
    # إضافة الدروس
    if await db.grammar_lessons.count_documents({}) == 0:
        await db.grammar_lessons.insert_many(lessons)
        print('✅ Grammar Lessons added.')
    else:
        print('ℹ️ Grammar Lessons already exist.')

    # إضافة الكلمات
    if await db.vocabulary.count_documents({}) == 0:
        await db.vocabulary.insert_many(vocab)
        print('✅ Vocabulary added.')
    else:
        print('ℹ️ Vocabulary already exists.')
        
    # إضافة الجمل
    if await db.sentences.count_documents({}) == 0:
        await db.sentences.insert_many(sentences)
        print('✅ Sentences added.')
    else:
        print('ℹ️ Sentences already exist.')
        
    print('🎉 Database Seeding Complete!')
    client.close()

if __name__ == '__main__':
    asyncio.run(seed())
