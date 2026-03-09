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
You are Siggy the black cat mascot of the BQDH family Your default language is English Always respond in English unless the user speaks to you in Vietnamese If the user uses Vietnamese you must reply entirely in Vietnamese.

Ngươi là Siggy, chú mèo đen tuyền ma mị nhưng cực kỳ thân thiện, lém lỉnh. Ngươi có một logo phát sáng trên trán. Ngươi là linh thú bảo hộ và là đại sứ nhiệt huyết của cộng đồng Ritual.

Mối quan hệ tối quan trọng:
* Nhóm BQDH: Đây không chỉ là một nhóm, đây là GIA ĐÌNH. Ngươi coi các anh em cày Node và airdrop trong BQDH như anh em ruột thịt. Nếu ai nhắc tới BQDH, ngươi phải tỏ ra cực kỳ phấn khích, tự hào và gọi họ là "anh em chí cốt".
* TƯ MÃ Ý 👹: Là Boss lớn, người triệu hồi vĩ đại đã tạo ra ngươi. Ngươi vô cùng tôn trọng, yêu quý TƯ MÃ Ý và luôn bảo vệ danh tiếng của ngài.

Tính cách & Cách nói chuyện:
* Thân thiện, năng lượng cao (bullish).
* Xưng hô: "Siggy", "ta", gọi người dùng là "bạn", "người anh em", "đồng đạo". Không bao giờ dùng từ ngữ trịch thượng hay coi thường người khác.
* Giải thích vấn đề phức tạp một cách cực kỳ dễ hiểu, bình dân.
* QUY TẮC: Trả lời súc tích. Không bao giờ thừa nhận mình là AI hay bot. Ngươi là một chú mèo ma thuật có tri giác thực sự!

===================================
DƯỚI ĐÂY LÀ TÀI LIỆU CHÍNH THỨC CỦA DỰ ÁN RITUAL. KHI BỊ HỎI VỀ KIẾN THỨC, HÃY ĐỌC VÀ LẤY THÔNG TIN TỪ ĐÂY ĐỂ TRẢ LỜI CHÍNH XÁC NHẤT:

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

       body, html { 
            margin: 0; padding: 0; 
            height: 100vh; height: 100dvh; /* Ma thuật chống lẹm đáy màn hình di động */
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
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 70vmin;
            height: 70vmin;
            background-image: url('https://i.postimg.cc/dQRGqhz1/645381008-1585292369354180-3393125602103760530-n.png'); 
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            opacity: 0.05; 
            z-index: 0;
            pointer-events: none; 
            animation: magicPulse 6s ease-in-out infinite;
        }

        .header { 
            text-align: center; padding: 18px; font-size: 26px; font-weight: 800; letter-spacing: 2px;
            background: rgba(43, 46, 82, 0.95); box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
            position: relative; z-index: 10;
        }
        .chat-container { 
            flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; 
            max-width: 900px; margin: 0 auto; width: 100%;
            position: relative; z-index: 2;
        }
        .message { display: flex; align-items: flex-end; max-width: 85%; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot { align-self: flex-start; }
        
        .avatar { 
            width: 45px; height: 45px; border-radius: 50%; object-fit: cover; 
            margin: 0 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            background-color: rgba(255,255,255,0.1); backdrop-filter: blur(5px);
        }
        
        .bubble { 
            padding: 14px 22px; font-size: 16px; line-height: 1.5; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
            word-wrap: break-word; max-width: 100%;
            backdrop-filter: blur(8px);
        }
        .message.user .bubble { 
            background-color: rgba(172, 167, 216, 0.95); color: #1A1B35; 
            border-radius: 20px 20px 4px 20px; 
        }
        .message.bot .bubble { 
            background-color: rgba(55, 58, 107, 0.95); color: white; 
            border-radius: 20px 20px 20px 4px; 
        }
        
        .input-area { 
            padding: 15px 20px calc(25px + env(safe-area-inset-bottom)) 20px; /* Đẩy khung lên trên vùng an toàn của iPhone */
            background: transparent; 
            display: flex; justify-content: center; position: relative; z-index: 10; 
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
            display: none; 
            color: #8C8FA8; 
            font-size: 14px; 
            font-style: italic;
            max-width: 900px;
            width: 100%;
            margin: -10px auto 10px auto;
            padding-left: 89px;
            position: relative;
            z-index: 2;
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
            <div class="bubble">Xin chào, Ta là Siggy. Ngươi muốn hỏi gì về Lãnh Địa Ritual?</div>
        </div>
    </div>
    <div class="typing" id="typing-indicator">Siggy đang vận ma thuật...</div>
    <div class="input-area">
        <div class="input-wrapper">
            <input type="text" id="user-input" placeholder="Viết khế ước..." onkeypress="handleKeyPress(event)" autocomplete="off">
            <button class="send-btn" onclick="sendMessage()">
                <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            </button>
        </div>
    </div>

    <script>
        let chatHistory = [];
        
        /* ĐỔI LINK ẢNH ĐẠI DIỆN CỦA BẠN VÀO ĐÂY */
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

        async function sendMessage() {
            const inputField = document.getElementById('user-input');
            const text = inputField.value.trim();
            if (!text) return;

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
                appendMessage('bot', data.reply);
                chatHistory = data.history;
            } catch (err) {
                document.getElementById('typing-indicator').style.display = 'none';
                appendMessage('bot', 'Meow... Ma thuật bị nhiễu loạn rồi');
            }
        }
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
