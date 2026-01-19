<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrou App</title>
    <style>
        :root { --main-bg: #4e54c8; --card-bg: rgba(255,255,255,0.15); }
        body { background: linear-gradient(to bottom, #4e54c8, #8f94fb); color: white; font-family: sans-serif; margin: 0; text-align: center; }
        
        /* تصميم البطاقات العلوية */
        .stats-container { display: flex; justify-content: center; gap: 10px; padding: 20px; }
        .stat-box { background: var(--card-bg); padding: 15px; border-radius: 15px; width: 80px; backdrop-filter: blur(5px); }
        
        /* مسار المترو (نظام Subway Surfers) */
        .metro-track { height: 10px; background: #333; margin: 50px 20px; position: relative; display: flex; justify-content: space-between; align-items: center; border-radius: 5px; }
        .station { width: 40px; height: 40px; background: #fff; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #333; font-weight: bold; border: 4px solid #4CAF50; transition: 0.3s; }
        .locked { border-color: #555; background: #888; cursor: not-allowed; }

        /* شاشة المفتش (الكمين المفاجئ) */
        #inspector-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); display: none; z-index: 1000; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .punishment { color: #ff5252; font-style: italic; margin-top: 20px; }
    </style>
</head>
<body>

    <h2>مرحباً، Omer! 👋</h2>
    # إضافة متغيرات الحالة (في الإنتاج يفضل ربطها بـ MongoDB)
user_stats = {
    "energy": 5,
    "points": 0,
    "last_check": None
}

@api_router.get("/user/stats")
async def get_stats():
    return user_stats

@api_router.post("/ai/inspect/fail")
async def handle_fail():
    if user_stats["energy"] > 0:
        user_stats["energy"] -= 1
    return {"message": "خصم طاقة!", "current_energy": user_stats["energy"]}

    
    <div class="stats-container">
        <div class="stat-box">⚡<br>5<br><small>طاقة</small></div>
        <div class="stat-box">⭐<br>0<br><small>نقطة</small></div>
        <div class="stat-box">🔥<br>0<br><small>توالي</small></div>
    </div>

    <div class="metro-track">
        <div class="station" onclick="startLesson('الترحيب')">1</div>
        <div class="station locked" onclick="checkInspector('الأفعال')">🔒</div>
        <div class="station locked" onclick="checkInspector('القواعد')">🔒</div>
    </div>

    <div id="inspector-screen">
        <h1 style="font-size: 80px;">👮‍♂️</h1>
        <h2 style="color: #ff5252;">تفتيش مفاجئ!</h2>
        <p id="inspection-task">أظهر تذكرتك اللغوية.. المفتش يراجع دروسك السابقة!</p>
        <div id="ai-question" style="background: #222; padding: 20px; border-radius: 10px; border: 1px solid #4CAF50;"></div>
        <p class="punishment" id="punishment-text"></p>
        <button onclick="closeInspector()" style="margin-top:20px; padding: 10px 30px; border-radius: 20px; border: none; background: #4CAF50; color: white;">تم التنفيذ 😅</button>
    </div>

    <script>
        const API_URL = "https://metrou-db.onrender.com";
        let lastLesson = "الترحيب";

        async function checkInspector(nextStation) {
            const screen = document.getElementById('inspector-screen');
            const questionDiv = document.getElementById('ai-question');
            
            screen.style.display = 'flex';
            questionDiv.innerText = "جاري استدعاء المفتش... 🏃‍♂️";

            try {
                // استدعاء Gemini لتوليد سؤال تفتيش بناءً على ما تعلمته
                const res = await fetch(`${API_URL}/api/ai/inspect`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({ lesson: lastLesson })
                });
                const data = await res.json();
                questionDiv.innerText = data.question;
                document.getElementById('punishment-text').innerText = "العقاب إذا أخطأت: " + data.punishment;
            } catch (e) {
                questionDiv.innerText = "المفتش سمح لك بالمرور هذه المرة مجاناً! 🏃‍♂️";
            }
        }

        function closeInspector() {
            document.getElementById('inspector-screen').style.display = 'none';
        }
    </script>
</body>
</html>
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
        @app.on_event("startup")
async def startup_event():
    # التحقق من وجود بيانات، وإذا لم توجد نقوم بإضافتها
    count = await db["lessons"].count_documents({})
    if count == 0:
        sample_lessons = [
            {
                "id": "L1",
                "level": 1,
                "title": "الترحيب والتعارف",
                "content": "تعلم كيف تقول مرحباً بالفرنسية: Bonjour",
                "order": 1
            },
            {
                "id": "L2",
                "level": 1,
                "title": "الأرقام من 1 إلى 10",
                "content": "Un, Deux, Trois...",
                "order": 2
            }
        ]
        await db["lessons"].insert_many(sample_lessons)
        
        sample_words = [
            {"french": "Bonjour", "arabic": "صباح الخير / مرحباً", "level": 1},
            {"french": "Merci", "arabic": "شكراً", "level": 1}
        ]
        await db["vocabulary"].insert_many(sample_words)
        print("تم حقن البيانات الأولية بنجاح! ✅")
