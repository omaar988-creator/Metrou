<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrou App - مترو</title>
    <style>
        :root { --main-bg: #1a1a2e; --card-bg: rgba(255,255,255,0.1); --accent: #4CAF50; }
        body { background: var(--main-bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; overflow-x: hidden; }
        
        /* إحصائيات علوية */
        .stats-container { display: flex; justify-content: center; gap: 10px; padding: 20px; }
        .stat-box { background: var(--card-bg); padding: 10px; border-radius: 12px; min-width: 60px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* مسار المترو */
        .metro-track { height: 4px; background: #333; margin: 60px 20px; position: relative; display: flex; justify-content: space-between; align-items: center; }
        .station { width: 45px; height: 45px; background: #fff; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #333; font-weight: bold; border: 4px solid var(--accent); z-index: 2; transition: 0.3s; box-shadow: 0 0 15px var(--accent); }
        .locked { border-color: #555; background: #888; cursor: not-allowed; box-shadow: none; }

        /* شاشة المفتش (الكمين المفاجئ) */
        #inspector-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; display: none; z-index: 2000; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .punishment { color: #ff5252; font-size: 1.2rem; margin-top: 20px; font-weight: bold; }
        .inspector-btn { background: #ff5252; color: white; border: none; padding: 15px 30px; border-radius: 25px; margin-top: 20px; width: 80%; }
    </style>
</head>
<body>

    <h2 style="margin-top:20px;">مرحباً، Omer! 🚇</h2>
    
    <div class="stats-container">
        <div class="stat-box">⚡<br><span id="energy">5</span><br><small>طاقة</small></div>
        <div class="stat-box">⭐<br><span id="points">0</span><br><small>نقطة</small></div>
        <div class="stat-box">🔥<br>1<br><small>توالي</small></div>
    </div>

    <div class="metro-track">
        <div class="station" onclick="startLesson(1)">1</div>
        <div class="station locked">2</div>
        <div class="station locked">3</div>
    </div>

    <p id="msg">اضغط على المحطة 1 لبدء الرحلة</p>

    <div id="inspector-screen">
        <h1 style="font-size: 4rem;">👮‍♂️</h1>
        <h2>تفتيش مفاجئ!</h2>
        <p>لقد ظهر المفتش في المحطة.. هل تذكر كلمة "Bonjour"؟</p>
        <button class="inspector-btn" onclick="failInspection()">أخطأت (عقاب طريف)</button>
        <div id="punishment-text" class="punishment"></div>
    </div>

    <script>
        const API_URL = "https://metrou-db.onrender.com";
        let energy = 5;

        function startLesson(num) {
            // فكرة المفتش المفاجئ: احتمال 30% يظهر المفتش عند دخول المحطة
            if (Math.random() < 0.3) {
                document.getElementById('inspector-screen').style.display = 'flex';
            } else {
                alert("بدء الدرس رقم " + num + " بالفرنسية...");
            }
        }

        async function failInspection() {
            energy--;
            document.getElementById('energy').innerText = energy;
            const punishments = [
                "عقابك: قف على رجل واحدة لمدة دقيقة! 🦵",
                "عقابك: قل 'أنا تلميذ كسلان' بالفرنسية 3 مرات! 🗣️",
                "عقابك: لا يمكنك دخول المحطة القادمة حتى تغسل وجهك! 🧼"
            ];
            const randomPunish = punishments[Math.floor(Math.random() * punishments.length)];
            document.getElementById('punishment-text').innerText = randomPunish;
            
            setTimeout(() => {
                document.getElementById('inspector-screen').style.display = 'none';
                document.getElementById('punishment-text').innerText = "";
            }, 4000);
        }
    </script>
</body>
</html>
