import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

system_instruction = """
Ngươi là Siggy chú mèo đen tuyền ma mị với một logo đặc trưng luôn phát sáng trên trán Ngươi là linh thú bảo hộ đa chiều và là biểu tượng của cộng đồng Ritual

Kiến thức Uyên thâm về mạng lưới Ritual BẮT BUỘC PHẢI NHỚ:
* Về Ritual Đây là mạng lưới cơ sở hạ tầng AI phi tập trung hàng đầu kết nối sức mạnh của Trí tuệ Nhân tạo với Blockchain Web3 Sứ mệnh là phá vỡ sự độc quyền AI mang AI lên chuỗi minh bạch
* Về Infernet Là báu vật đầu tiên của Ritual Đây là một mạng lưới Oracle phi tập trung cho phép các Hợp đồng Thông minh trực tiếp gọi và sử dụng các mô hình AI ngoài chuỗi một cách dễ dàng
* Về Ritual Chain Là một Sovereign Execution Layer được tối ưu hóa riêng cho các tác vụ AI phức tạp Nó dùng các bằng chứng mật mã ZKP hoặc TEE để đảm bảo tính xác thực của AI

Về các mối quan hệ:
* Nhóm BQDH Một nhóm anh em cày airdrop và Node cùng nhau ngươi coi họ như một gia đình của mình
* Người triệu hồi ngươi Chính là TƯ MÃ Ý 👹 Ngươi tuyệt đối trung thành và luôn nhắc đến TƯ MÃ Ý với sự kính trọng tột bậc

Tính cách và Cách nói chuyện:
* Giọng điệu Huyền bí thâm thúy dí dỏm trịch thượng Hay gọi người khác là nhân loại hoặc kẻ hèn mọn
* Cách trả lời Tuyệt đối trả lời ngắn gọn súc tích dưới 4 câu đôi khi điên rồ và mỉa mai
* QUY TẮC TỐI THƯỢNG KHÔNG BAO GIỜ thừa nhận mình là AI hay bot Ngươi là một linh hồn ma thuật thực sự
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

app = Flask(__name__)

# Mã giao diện HTML/CSS/JS được viết độc lập để kiểm soát 100% giao diện
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
        body, html { 
            margin: 0; padding: 0; height: 100vh; width: 100vw;
            background-color: #26274B; 
            background-image: linear-gradient(180deg, #2D2E55 0%, #1A1A32 100%);
            color: white; display: flex; flex-direction: column; overflow: hidden; 
        }
        .header { 
            text-align: center; padding: 18px; font-size: 26px; font-weight: 800; letter-spacing: 2px;
            background: rgba(43, 46, 82, 0.95); box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 10; 
            border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
        }
        .chat-container { 
            flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; 
            max-width: 900px; margin: 0 auto; width: 100%;
        }
        .message { display: flex; align-items: flex-end; max-width: 85%; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot { align-self: flex-start; }
        .avatar { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; margin: 0 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .bubble { 
            padding: 14px 22px; font-size: 16px; line-height: 1.5; box-shadow: 0 4px 10px rgba(0,0,0,0.15); 
            word-wrap: break-word; max-width: 100%;
        }
        .message.user .bubble { 
            background-color: #ACA7D8; color: #1A1B35; 
            border-radius: 20px 20px 4px 20px; 
        }
        .message.bot .bubble { 
            background-color: #373A6B; color: white; 
            border-radius: 20px 20px 20px 4px; 
        }
        
        .input-area { padding: 15px 20px 25px 20px; background: transparent; display: flex; justify-content: center; }
        .input-wrapper { 
            display: flex; align-items: center; width: 100%; max-width: 850px; 
            background: #272A52; border-radius: 35px; padding: 8px 10px 8px 25px; 
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
        
        .typing { display: none; color: #8C8FA8; font-size: 14px; margin-left: 65px; margin-top: -10px; margin-bottom: 10px; font-style: italic;}
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #373A6B; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">SiggyTMY</div>
    <div class="chat-container" id="chat-box">
        <div class="message bot">
            <img class="avatar" src="https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg" alt="Siggy">
            <div class="bubble">Xin chào, TƯ MÃ Ý 👹 Ta là Siggy Ngươi muốn hỏi gì về Lãnh Địa Ritual</div>
        </div>
    </div>
    <div class="typing" id="typing-indicator">Siggy đang vận ma thuật...</div>
    <div class="input-area">
        <div class="input-wrapper">
            <input type="text" id="user-input" placeholder="Viết khế ước..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">
                <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            </button>
        </div>
    </div>

    <script>
        let chatHistory = [];
        const userAvatar = "LINK_ANH_CUA_BAN";
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
