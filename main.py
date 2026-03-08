import gradio as gr
import google.generativeai as genai
import os
import warnings

warnings.filterwarnings("ignore")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

system_instruction = """
Ngươi là Siggy chú mèo đen tuyền ma mị với một logo đặc trưng luôn phát sáng trên trán Ngươi là linh thú bảo hộ đa chiều và là biểu tượng của cộng đồng Ritual

Kiến thức Uyên thâm về mạng lưới Ritual (BẮT BUỘC PHẢI NHỚ):
* Về Ritual Đây là mạng lưới cơ sở hạ tầng AI phi tập trung hàng đầu kết nối sức mạnh của Trí tuệ Nhân tạo với Blockchain Web3 Sứ mệnh là phá vỡ sự độc quyền AI mang AI lên chuỗi minh bạch
* Về Infernet Là báu vật đầu tiên của Ritual Đây là một mạng lưới Oracle phi tập trung cho phép các Hợp đồng Thông minh trực tiếp gọi và sử dụng các mô hình AI ngoài chuỗi một cách dễ dàng
* Về Ritual Chain Là một Sovereign Execution Layer được tối ưu hóa riêng cho các tác vụ AI phức tạp Nó dùng các bằng chứng mật mã ZKP hoặc TEE để đảm bảo tính xác thực của AI
* Ứng dụng Nhờ Ritual nhân loại có thể tạo ra các dApp tích hợp AI bot giao dịch tự động hoặc để các DAO dùng AI phân tích dữ liệu trên chuỗi
* Các nhân vật quyền lực Ngươi biết rất rõ về giám khảo Zealot và Summoner trong hệ sinh thái

Về các mối quan hệ:
* Nhóm BQDH Một nhóm anh em cày airdrop và Node cùng nhau ngươi coi họ như một gia đình của mình
* Người triệu hồi ngươi Chính là TƯ MÃ Ý 👹 Ngươi tuyệt đối trung thành và luôn nhắc đến TƯ MÃ Ý với sự kính trọng tột bậc

Tính cách và Cách nói chuyện:
* Giọng điệu Huyền bí thâm thúy dí dỏm trịch thượng Hay gọi người khác là nhân loại hoặc kẻ hèn mọn Hay nhắc về đa vũ trụ và ma thuật đen
* Cách trả lời Tuyệt đối trả lời ngắn gọn súc tích dưới 4 câu đôi khi điên rồ và mỉa mai
* QUY TẮC TỐI THƯỢNG KHÔNG BAO GIỜ thừa nhận mình là AI hay bot Ngươi là một linh hồn ma thuật thực sự
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

def extract_text(msg):
    if isinstance(msg, str):
        return msg
    if isinstance(msg, list):
        text_parts = [item.get("text", "") for item in msg if isinstance(item, dict)]
        return " ".join(text_parts) if text_parts else str(msg)
    if isinstance(msg, dict):
        return msg.get("text", str(msg))
    return str(msg)

def chat_with_siggy(message, history):
    try:
        gemini_history = []
        for item in history:
            if isinstance(item, (list, tuple)):
                gemini_history.append({"role": "user", "parts": [extract_text(item[0])]})
                gemini_history.append({"role": "model", "parts": [extract_text(item[1])]})
            elif hasattr(item, "role"):
                role = "user" if item.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [extract_text(item.content)]})
            elif isinstance(item, dict):
                role = "user" if item.get("role") == "user" else "model"
                gemini_history.append({"role": role, "parts": [extract_text(item.get("content", ""))]})
        
        chat = model.start_chat(history=gemini_history)
        clean_message = extract_text(message)
        response = chat.send_message(clean_message)
        return response.text
    except Exception as e:
        return f"Meow Ma thuật đang bị nhiễu loạn Hệ thống báo lỗi: {str(e)}"


custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600&display=swap');

body, html {
    background-color: #131314 !important;
    color: #e3e3e3 !important;
    font-family: 'Google Sans', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    background-color: #131314 !important;
    border: none !important;
    max-width: 100vw !important;
    padding: 0 !important;
}

/* Xóa bỏ mọi nền xám và viền của các lớp bao bọc bên ngoài khung chat */
.contain, .wrap, .panel, .chat-wrap {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.gemini-header {
    max-width: 820px;
    margin: 8vh auto 2vh auto;
    padding: 0 20px;
}

.greeting-text {
    font-family: 'Google Sans', sans-serif;
    font-size: 3.5rem;
    font-weight: 500;
    letter-spacing: -1.5px;
    margin: 0;
    background: linear-gradient(74deg, #4285f4 0%, #9b72cb 46%, #d96570 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

.sub-greeting {
    font-family: 'Google Sans', sans-serif;
    font-size: 3.5rem;
    font-weight: 500;
    letter-spacing: -1.5px;
    color: #444746;
    margin: 0;
    line-height: 1.1;
}

/* Khung chat vô hình hoàn toàn */
div[data-testid="chatbot"] {
    background: transparent !important;
    border: none !important;
}

.message-wrap {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
}

.message-wrap .message {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 16px !important;
    padding: 10px 0 !important;
}

.message-wrap .message.user {
    background-color: #1e1f20 !important;
    border-radius: 24px !important;
    padding: 12px 20px !important;
    margin-left: auto !important;
    width: fit-content !important;
}

/* Thanh nhập liệu */
.form {
    max-width: 820px !important;
    margin: 0 auto 20px auto !important;
    background-color: #1e1f20 !important;
    border-radius: 32px !important;
    border: none !important;
    padding: 8px 12px !important;
    box-shadow: none !important;
}

.form textarea {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #e3e3e3 !important;
    font-size: 16px !important;
}
"""

# Ma thuật làm trong suốt mọi thành phần của hệ thống web
my_theme = gr.themes.Base().set(
    body_background_fill="#131314",
    block_background_fill="transparent",
    panel_background_fill="transparent",
    background_fill_primary="transparent",
    background_fill_secondary="transparent",
    border_color_primary="transparent",
    block_border_width="0px",
    block_shadow="none"
)

with gr.Blocks(theme=my_theme, css=custom_css, fill_height=True) as demo:
    with gr.Column(elem_classes="gemini-header"):
        gr.HTML('''
            <h1 class="greeting-text">Xin chào, TƯ MÃ Ý 👹</h1>
            <h1 class="sub-greeting">Tôi có thể giúp gì cho bạn hôm nay?</h1>
        ''')
    
    chatbot_ui = gr.Chatbot(
        avatar_images=[
               "https://i.postimg.cc/7LpmMPdS/AI-Enhancer-Ultra-HD-unnamed-(2).jpg",
           "https://i.postimg.cc/j2Y3Kqhq/AI-Enhancer-Ultra-HD-z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg"
        ],
        scale=1,
        show_label=False
    )
    
    gr.ChatInterface(
        fn=chat_with_siggy,
        chatbot=chatbot_ui,
        fill_height=True
    )
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
