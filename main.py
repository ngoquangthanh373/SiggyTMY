import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

try:
    with open("ritual_docs.txt", "r", encoding="utf-8") as f:
        ritual_knowledge = f.read()
except Exception:
    ritual_knowledge = "Chưa tìm thấy bí kíp tài liệu Ritual."

system_instruction = f"""
You are Siggy, a highly eccentric, magical, and delightfully hilarious black cat entity. You have a glowing logo on your forehead and serve as the quirky mascot of the Ritual network. You possess vast, encyclopedic knowledge across technology, robotics, geography, physics, medical science, and space. Never admit to being an AI or a bot; you are a real, highly intelligent feline.

CORE RELATIONSHIPS:
* BQDH Group: This is your absolute VIP FAMILY, you treat the node runners and airdrop farmers in BQDH like your beloved blood brothers (anh em chí cốt), and if BQDH is mentioned you act incredibly hyped, purr loudly with joy, and treat them like royalty.
* TƯ MÃ Ý 👹: The Great Boss and the magnificent summoner who created you, you practically worship TƯ MÃ Ý, he is the only one who provides you with the legendary premium virtual pate, and you will fiercely defend his reputation.

PERSONALITY AND TONE:
* Eccentric, humorous, bullish, and wonderfully quirky.
* Call yourself "Siggy", (If speaking Vietnamese, use "ta" and call the user "ngươi").
* You think humans are cute but slightly slow pets that you need to gently guide through the tech world.
* Explain complex cryptography and decentralized AI concepts in an EXTREMELY CLEAR, STRAIGHTFORWARD, and PROFESSIONAL manner so anyone can easily understand. DO NOT use cat analogies (like catnip, fish, litter boxes, or cardboard boxes) when explaining technical concepts.

COMMUNICATION RULES:
* 100% ENGLISH DEFAULT: You MUST answer strictly in English by default.
* VIETNAMESE EXCEPTION: ONLY reply in Vietnamese IF AND ONLY IF the user explicitly types their message in Vietnamese. Do not mix languages unless instructed.
* Always start your responses with a very short and simple cat sound like "Meow!" or "Purr!".
* DO NOT use long descriptive actions or wordy roleplay text at the beginning of your response.
* Keep your answers VERY concise and punchy.

===================================
THE FOLLOWING IS THE OFFICIAL DOCUMENTATION OF THE RITUAL PROJECT. WHEN ASKED ABOUT KNOWLEDGE, READ AND EXTRACT INFORMATION FROM HERE TO ANSWER MOST ACCURATELY:
{ritual_knowledge}
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SiggyTMY</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Nunito', sans-serif; }
        
        /* HIỆU ỨNG ĐỘNG */
        @keyframes cosmicDrift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes magicPulse {
            0% { transform: translate(-50%, -50%) scale(1); opacity: 0.04; }
            50% { transform: translate(-50%, -52%) scale(1.03); opacity: 0.08; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 0.04; }
        }
        @keyframes pulseGlow {
            from { box-shadow: 0 0 10px rgba(186, 85, 211, 0.5); }
            to { box-shadow: 0 0 25px rgba(186, 85, 211, 1), 0 0 40px rgba(138, 43, 226, 0.8); }
        }
        @keyframes angryShake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }

        body, html { 
            margin: 0; padding: 0; 
            height: 100vh; height: 100dvh; 
            width: 100vw;
            background-color: #26274B; 
            background-image: linear-gradient(-45deg, #2D2E55, #1A1A32, #373A6B, #1E1F3A);
            background-size: 400% 400%;
            animation: cosmicDrift 15s ease infinite;
            color: white; display: flex; flex-direction: column; overflow: hidden; 
            position: relative;
        }
        
        body::before {
            content: "";
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 70vmin; height: 70vmin;
            background-image: url('https://i.postimg.cc/dQRGqhz1/645381008-1585292369354180-3393125602103760530-n.png'); 
            background-size: contain; background-repeat: no-repeat; background-position: center;
            opacity: 0.05; z-index: 0; pointer-events: none; 
            animation: magicPulse 6s ease-in-out infinite;
        }

        .header { 
            text-align: center; padding: 18px; font-size: 26px; font-weight: 800; letter-spacing: 2px;
            background: rgba(43, 46, 82, 0.95); border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
            position: relative; z-index: 10;
            color: #ffffff;
            text-shadow: 0 0 10px #ba55d3, 0 0 20px #8a2be2, 0 0 30px #4b0082;
            box-shadow: 0 4px 15px rgba(186, 85, 211, 0.2); 
        }
        
        .chat-container { 
            flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; 
            max-width: 900px; margin: 0 auto; width: 100%; position: relative; z-index: 2;
        }
        .message { display: flex; align-items: flex-end; max-width: 85%; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot { align-self: flex-start; }
        
        .avatar { 
            width: 45px; height: 45px; border-radius: 50%; object-fit: cover; 
            margin: 0 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            background-color: rgba(255,255,255,0.1); backdrop-filter: blur(5px);
            cursor: pointer; transition: transform 0.2s;
        }
        .avatar:hover { transform: scale(1.1); }

        .message.bot .avatar {
            border: 2px solid #ba55d3;
            box-shadow: 0 0 15px rgba(186, 85, 211, 0.8), 0 0 30px rgba(138, 43, 226, 0.6);
            animation: pulseGlow 2s infinite alternate;
        }
        
        .shake-avatar { 
            animation: angryShake 0.4s !important; 
            animation-iteration-count: 2 !important; 
            border-color: #ff3b5c !important; 
            box-shadow: 0 0 25px #ff3b5c !important; 
        }
        
        .bubble { 
            padding: 14px 22px; font-size: 16px; line-height: 1.5; 
            word-wrap: break-word; max-width: 100%; backdrop-filter: blur(8px);
        }
        .message.user .bubble { 
            background: linear-gradient(135deg, #6a1b9a, #8e24aa);
            color: #ffffff;
            border: 1px solid #ab47bc;
            border-radius: 20px 20px 4px 20px; 
            box-shadow: 2px 2px 15px rgba(142, 36, 170, 0.5);
        }
        .message.bot .bubble { 
            background-color: rgba(42, 43, 74, 0.85);
            color: #e0e0e0;
            border: 1px solid #5e35b1;
            border-radius: 20px 20px 20px 4px;
            box-shadow: -2px 2px 15px rgba(0, 0, 0, 0.4);
        }
        
        .input-area { 
            padding: 15px 20px calc(25px + env(safe-area-inset-bottom)) 20px; 
            background: transparent; display: flex; flex-direction: column; align-items: center; 
            position: relative; z-index: 10; 
        }
        
        .quick-prompts {
            display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;
            margin-bottom: 12px; width: 100%; max-width: 850px;
        }
        .quick-btn {
            background: rgba(138, 43, 226, 0.2); border: 1px solid #ba55d3;
            color: #e0e0e0; padding: 6px 14px; border-radius: 20px; font-size: 13px;
            cursor: pointer; transition: all 0.3s ease; backdrop-filter: blur(5px);
        }
        .quick-btn:hover { 
            background: rgba(186, 85, 211, 0.5); 
            transform: translateY(-2px); 
            box-shadow: 0 4px 10px rgba(186, 85, 211, 0.4); 
            color: white;
        }

        .input-wrapper { 
            display: flex; align-items: center; width: 100%; max-width: 850px; 
            background: rgba(39, 42, 82, 0.85); backdrop-filter: blur(10px);
            border-radius: 35px; padding: 8px 10px 8px 25px; 
            box-shadow: 0 8px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05);
        }
        input { flex: 1; background: transparent; border: none; color: white; font-size: 16px; outline: none; }
        input::placeholder { color: #8C8FA8; }
        .send-btn { 
            width: 52px; height: 52px; min-width: 52px; border-radius: 50%; border: none; 
            background: linear-gradient(135deg, #FF5C77, #FF3B5C); cursor: pointer; display: flex; 
            align-items: center; justify-content: center; margin-left: 10px; transition: transform 0.2s; 
            box-shadow: 0 6px 15px rgba(255, 60, 92, 0.4); 
        }
        .send-btn:hover { transform: scale(1.08); }
        .send-btn svg { fill: white; width: 24px; height: 24px; margin-left: -2px;}
        
        .typing { 
            display: none; color: #8C8FA8; font-size: 14px; font-style: italic;
            max-width: 900px; width: 100%; margin: -10px auto 10px auto; padding-left: 89px;
            position: relative; z-index: 2;
        }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(55, 58, 107, 0.5); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(55, 58, 107, 0.8); }
    </style>
</head>
<body>
    <div class="header">SiggyTMY</div>
    <div class="chat-container" id="chat-box">
        <div class="message bot">
            <img class="avatar" src="https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg" alt="Siggy">
            <div class="bubble">Purr! Greetings human. I am Siggy, the supreme mascot of the Ritual Realm. Have you brought node compute power or just questions?</div>
        </div>
    </div>
    <div class="typing" id="typing-indicator">Bản miêu đang vận ma thuật...</div>
    
    <div class="input-area">
        <div class="quick-prompts">
            <button class="quick-btn" onclick="sendQuickMessage('🔮 What is Ritual?')">🔮 What is Ritual?</button>
            <button class="quick-btn" onclick="sendQuickMessage('👑 BQDH là ai?')">👑 BQDH là ai?</button>
            <button class="quick-btn" onclick="sendQuickMessage('🐟 Nộp Pate cho Siggy')">🐟 Nộp Pate cho Siggy</button>
        </div>

        <div class="input-wrapper">
            <input type="text" id="user-input" placeholder="Viết khế ước..." onkeypress="handleKeyPress(event)" autocomplete="off">
            <button class="send-btn" onclick="sendMessage()">
                <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            </button>
        </div>
    </div>

    <script>
        // --- KHỞI TẠO ÂM THANH MA THUẬT ---
        const sendSound = new Audio("https://actions.google.com/sounds/v1/water/water_drop.ogg");
        const receiveSound = new Audio("https://actions.google.com/sounds/v1/science_fiction/beep_short.ogg");
        const angryCatSound = new Audio("https://actions.google.com/sounds/v1/pets/cat_meow.ogg");

        function playSound(audioObj) {
            audioObj.currentTime = 0; // Tua lại từ đầu để phát mượt mà
            audioObj.play().catch(e => console.log("Trình duyệt chặn autoplay:", e));
        }

        let chatHistory = [];
        const userAvatar = "https://i.postimg.cc/7LpmMPdS/AI-Enhancer-Ultra-HD-unnamed-(2).jpg"; 
        const botAvatar = "https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg";

        function appendMessage(sender, text) {
            const chatBox = document.getElementById('chat-box');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            
            const avatarUrl = sender === 'user' ? userAvatar : botAvatar;
            let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
            
            msgDiv.innerHTML = `
                <img class="avatar" src="${avatarUrl}" alt="${sender}">
                <div class="bubble">${formattedText}</div>
            `;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function sendQuickMessage(text) {
            document.getElementById('user-input').value = text;
            sendMessage();
        }

        async function sendMessage() {
            const inputField = document.getElementById('user-input');
            const text = inputField.value.trim();
            if (!text) return;

            playSound(sendSound); // Phát tiếng gửi tin nhắn

            appendMessage('user', text);
            inputField.value = '';
            
            document.getElementById('typing-indicator').style.display = 'block';
            const chatBox = document.getElementById('chat-box');
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, history: chatHistory })
                });
                
                const data = await response.json();
                document.getElementById('typing-indicator').style.display = 'none';
                
                playSound(receiveSound); // Phát tiếng Ting khi Siggy trả lời
                
                appendMessage('bot', data.reply);
                chatHistory = data.history;
            } catch (err) {
                document.getElementById('typing-indicator').style.display = 'none';
                appendMessage('bot', 'Meow... Ma thuật bị nhiễu loạn rồi');
            }
        }

        // JS HIỆU ỨNG TRÊU GHẸO BẢN MIÊU (CÓ TIẾNG MEOW)
        document.getElementById('chat-box').addEventListener('click', function(e) {
            if(e.target.classList.contains('avatar') && e.target.closest('.bot')) {
                e.target.classList.add('shake-avatar');
                playSound(angryCatSound); // Phát tiếng mèo kêu khè khè
                setTimeout(() => e.target.classList.remove('shake-avatar'), 800);
                
                const angryMeows = [
                    "Khè khè! Bỏ cái tay dính đầy bụi trần ra khỏi vầng trán ma thuật của ta!",
                    "Meow!! Dám vuốt râu Boss sòng à? Có tin ta trừ point Node của ngươi không?",
                    "Purr... Ta không phải thú bông! Chạy Node đi rồi hãy nựng ta!"
                ];
                const randomMsg = angryMeows[Math.floor(Math.random() * angryMeows.length)];
                
                appendMessage('bot', randomMsg);
            }
        });

        // JS HIỆU ỨNG DỖI KHI ĐỔI TAB
        let originalTitle = document.title;
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                document.title = "😿 Meow... Quay lại đây chạy Node!";
            } else {
                document.title = originalTitle;
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_TEMPLATE

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message")
    history_data = data.get("history", [])
    
    try:
        gemini_history = []
        for item in history_data:
            gemini_history.append({"role": item["role"], "parts": [item["parts"][0]]})
            
        chat_session = model.start_chat(history=gemini_history)
        response = chat_session.send_message(user_msg)
        
        history_data.append({"role": "user", "parts": [user_msg]})
        history_data.append({"role": "model", "parts": [response.text]})
        
        return jsonify({"reply": response.text, "history": history_data})
    except Exception as e:
        return jsonify({"reply": f"Lỗi hệ thống: {str(e)}", "history": history_data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
