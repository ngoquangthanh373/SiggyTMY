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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

/* NỀN TẢNG VŨ TRỤ TRÀN VIỀN TUYỆT ĐỐI */
:root, body, html {
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    width: 100vw !important;
    background-color: #26274B !important;
    background-image: linear-gradient(180deg, #2D2E55 0%, #1A1A32 100%) !important;
    font-family: 'Nunito', sans-serif !important;
    overflow: hidden !important;
}

/* XÓA SỔ MỌI HỘP XÁM CỦA GRADIO */
.gradio-container, .main, .wrap, .contain, .panel, .chat-wrap, #component-0 {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    max-width: 100vw !important;
    padding: 0 !important;
}

footer { display: none !important; }

/* HEADER CỐ ĐỊNH Ở TRÊN CÙNG */
.cosmic-header {
    position: fixed;
    top: 0; left: 0; width: 100%;
    background-color: #313360;
    color: white;
    text-align: center;
    padding: 16px 0;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 2px;
    border-bottom-left-radius: 20px;
    border-bottom-right-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    z-index: 1000;
}

/* KHUNG CHAT ĐẨY XUỐNG DƯỚI HEADER VÀ GIỮA MÀN HÌNH */
.contain { 
    margin-top: 70px !important; 
    height: calc(100vh - 70px) !important;
}

div[data-testid="chatbot"] {
    background: transparent !important;
    border: none !important;
}

.message-wrap {
    padding: 20px !important;
    max-width: 850px !important;
    margin: 0 auto !important;
}

/* KIỂU DÁNG BONG BÓNG TIN NHẮN (TRÒN MỘT BÊN CHUẨN ẢNH GỐC) */
.message {
    font-size: 15px !important;
    padding: 14px 22px !important;
    margin-bottom: 20px !important;
    line-height: 1.5 !important;
}

/* Bot (Mèo Siggy) - Xanh thẫm, bẹt ở đuôi trái */
.message.bot {
    background-color: #373A6B !important;
    color: #FFFFFF !important;
    border-radius: 20px 20px 20px 4px !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
}

/* User (TƯ MÃ Ý) - Tím nhạt, bẹt ở đuôi phải */
.message.user {
    background-color: #ACA7D8 !important;
    color: #1A1B35 !important;
    border-radius: 20px 20px 4px 20px !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
    margin-left: auto !important;
}

/* Avatar tròn trịa */
.avatar-image {
    border-radius: 50% !important;
    background: transparent !important;
}

/* KHU VỰC NHẬP LIỆU LƠ LỬNG Ở ĐÁY */
.form {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    max-width: 850px !important;
    margin: 0 auto 20px auto !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    gap: 15px !important;
    padding: 0 20px !important;
}

/* Khung gõ chữ (Nhộng dài) */
.form textarea {
    background-color: #272A52 !important;
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
    box-shadow: none !important;
}
.form textarea::placeholder { color: #8C8FA8 !important; }

/* NÚT GỬI MÀU HỒNG TRÒN XOEA CHUẨN ẢNH GỐC */
button[aria-label="Submit"], .form button {
    background: linear-gradient(135deg, #FF5C77, #FF3B5C) !important;
    border-radius: 50% !important;
    width: 56px !important;
    height: 56px !important;
    min-width: 56px !important;
    border: none !important;
    box-shadow: 0 6px 15px rgba(255, 60, 92, 0.4) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform 0.2s ease !important;
}

button[aria-label="Submit"]:hover, .form button:hover {
    transform: scale(1.08) !important;
}

button[aria-label="Submit"] svg, .form button svg {
    fill: white !important;
    stroke: white !important;
    width: 24px !important;
    height: 24px !important;
    margin-left: -2px !important; /* Căn giữa icon máy bay */
}
"""

my_theme = gr.themes.Base().set(
    body_background_fill="transparent",
    block_background_fill="transparent",
    panel_background_fill="transparent",
    border_color_primary="transparent",
    block_border_width="0px"
)

with gr.Blocks(theme=my_theme, css=custom_css, fill_height=True) as demo:
    # Header SiggyTMY thay thế Poly
    gr.HTML('<div class="cosmic-header">SiggyTMY</div>')
    
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
