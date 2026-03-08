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

# Giao diện tối giản mô phỏng hoàn hảo Gemini Dark Mode
my_theme = gr.themes.Default(
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    text_size="lg",
).set(
    body_background_fill="#131314",
    body_text_color="#e3e3e3",
    block_background_fill="#131314",
    block_border_width="0px",
    input_background_fill="#1e1f20",
    input_border_color="#1e1f20",
    button_primary_background_fill="#1e1f20",
    button_primary_background_fill_hover="#333538",
    button_primary_text_color="#e3e3e3",
)

custom_css = """
body, html {
    background-color: #131314 !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    width: 100vw !important;
    overflow-x: hidden !important;
}
.gradio-container {
    max-width: 100vw !important;
    width: 100vw !important;
    min-height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Ép tin nhắn trong suốt, xóa bong bóng chat */
.message-wrap .message {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
    padding-top: 20px !important;
    padding-bottom: 20px !important;
}
/* Thu gọn thanh nhập liệu ở giữa màn hình */
.form {
    max-width: 800px !important;
    margin: 0 auto !important;
    border-radius: 24px !important;
    overflow: hidden !important;
    background-color: #1e1f20 !important;
}
"""

with gr.Blocks(theme=my_theme, css=custom_css, fill_height=True) as demo:
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
        fill_height=True,
        examples=["Ngươi là ai?", "TƯ MÃ Ý 👹 là ai đối với ngươi?", "Ritual là gì Infernet hoạt động ra sao?"]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
