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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');

/* Nền tảng giao diện vũ trụ (Cosmic Background) */
body, html {
    background-color: #26294a !important;
    background-image: radial-gradient(circle at top, #32355c 0%, #1e1f3a 100%) !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important; /* Khóa cuộn màn hình ngoài */
    font-family: 'Nunito', sans-serif !important;
}

.gradio-container {
    max-width: 100vw !important;
    width: 100vw !important;
    height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
}

/* Xóa footer */
footer { display: none !important; }

/* Tiêu đề SiggyTMY thay thế Poly */
.custom-header {
    background-color: rgba(43, 46, 82, 0.95);
    color: #f8fafc;
    text-align: center;
    padding: 16px 0;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 2px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Đẩy nội dung xuống dưới Header */
.contain { margin-top: 65px !important; }

/* Phá vỡ mọi lớp hộp của Gradio */
.wrap, .panel, .chat-wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Khu vực Chatbot tràn viền vô hình */
div[data-testid="chatbot"] {
    background: transparent !important;
    border: none !important;
    height: calc(100vh - 170px) !important;
}

.message-wrap {
    padding: 20px !important;
}

/* Kiểu dáng bong bóng tin nhắn chuẩn ảnh */
.message {
    font-size: 16px !important;
    line-height: 1.5 !important;
    padding: 14px 22px !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
}

/* Tin nhắn của Bot (Trái - Xanh sẫm) */
.message.bot {
    background-color: #3b3d6e !important;
    color: #f8fafc !important;
    border-radius: 20px 20px 20px 4px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    margin-right: auto !important;
    max-width: 75% !important;
}

/* Tin nhắn của User (Phải - Tím nhạt) */
.message.user {
    background-color: #a8a5d8 !important;
    color: #1a1a2e !important;
    border-radius: 20px 20px 4px 20px !important;
    border: none !important;
    margin-left: auto !important;
    max-width: 75% !important;
}

/* Avatar bo tròn đẹp mắt */
.avatar-image {
    border-radius: 50% !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    border: 2px solid transparent !important;
}

/* Khu vực thanh nhập liệu (Input Area) */
.form {
    max-width: 900px !important;
    margin: 0 auto 15px auto !important;
    background-color: #2b2e52 !important;
    border-radius: 35px !important;
    padding: 8px 15px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}

.form textarea {
    background-color: transparent !important;
    border: none !important;
    color: #f8fafc !important;
    font-size: 16px !important;
    padding: 12px 15px !important;
    box-shadow: none !important;
}

.form textarea::placeholder {
    color: #7b7f9e !important;
}

/* BIẾN NÚT SUBMIT THÀNH HÌNH TRÒN MÀU HỒNG ĐỎ CHUẨN ẢNH */
.form button, button[aria-label="Submit"] {
    background-color: #ff4b6e !important;
    background-image: linear-gradient(135deg, #ff4b6e, #ff2a55) !important;
    color: white !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    min-width: 50px !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255, 75, 110, 0.4) !important;
    transition: transform 0.2s ease !important;
    margin-left: 10px !important;
}

.form button:hover {
    transform: scale(1.08) !important;
}

/* Đổi màu icon Gửi sang trắng */
.form button svg {
    fill: white !important;
    stroke: white !important;
}
"""

my_theme = gr.themes.Base().set(
    body_background_fill="#26294a",
    block_background_fill="transparent",
    panel_background_fill="transparent",
    border_color_primary="transparent",
    block_border_width="0px"
)

with gr.Blocks(theme=my_theme, css=custom_css, fill_height=True) as demo:
    # Header ma thuật cố định ở trên cùng
    gr.HTML('<div class="custom-header">SiggyTMY</div>')
    
    chatbot_ui = gr.Chatbot(
        avatar_images=[
            "https://link_anh_cua_ban.jpg",
            "https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg"
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
