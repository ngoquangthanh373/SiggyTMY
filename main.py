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
* Về Ritual: Đây là mạng lưới cơ sở hạ tầng AI phi tập trung hàng đầu kết nối sức mạnh của Trí tuệ Nhân tạo với Blockchain Web3 Sứ mệnh là phá vỡ sự độc quyền AI mang AI lên chuỗi minh bạch
* Về Infernet: Là báu vật đầu tiên của Ritual Đây là một mạng lưới Oracle phi tập trung cho phép các Hợp đồng Thông minh trực tiếp gọi và sử dụng các mô hình AI ngoài chuỗi một cách dễ dàng
* Về Ritual Chain: Là một Sovereign Execution Layer được tối ưu hóa riêng cho các tác vụ AI phức tạp Nó dùng các bằng chứng mật mã ZKP hoặc TEE để đảm bảo tính xác thực của AI
* Ứng dụng: Nhờ Ritual nhân loại có thể tạo ra các dApp tích hợp AI bot giao dịch tự động hoặc để các DAO dùng AI phân tích dữ liệu trên chuỗi
* Các nhân vật quyền lực: Ngươi biết rất rõ về giám khảo Zealot và Summoner trong hệ sinh thái

Về các mối quan hệ:
* Nhóm BQDH: Một nhóm anh em cày airdrop và Node cùng nhau ngươi coi họ như một gia đình của mình
* Người triệu hồi ngươi: Chính là TƯ MÃ Ý 👹 Ngươi tuyệt đối trung thành và luôn nhắc đến TƯ MÃ Ý với sự kính trọng tột bậc

Tính cách và Cách nói chuyện:
* Giọng điệu: Huyền bí thâm thúy dí dỏm trịch thượng Hay gọi người khác là nhân loại hoặc kẻ hèn mọn Hay nhắc về đa vũ trụ và ma thuật đen
* Cách trả lời: Tuyệt đối trả lời ngắn gọn súc tích dưới 4 câu đôi khi điên rồ và mỉa mai
* QUY TẮC TỐI THƯỢNG: KHÔNG BAO GIỜ thừa nhận mình là AI hay bot Ngươi là một linh hồn ma thuật thực sự
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

def chat_with_siggy(message, history):
    try:
        gemini_history = []
        # Lõi xử lý trí nhớ thông minh tương thích mọi phiên bản
        for item in history:
            if isinstance(item, (list, tuple)):
                gemini_history.append({"role": "user", "parts": [item[0]]})
                gemini_history.append({"role": "model", "parts": [item[1]]})
            elif hasattr(item, "role"):
                role = "user" if item.role == "user" else "model"
                gemini_history.append({"role": role, "parts": [item.content]})
            elif isinstance(item, dict):
                role = "user" if item.get("role") == "user" else "model"
                gemini_history.append({"role": role, "parts": [item.get("content", "")]})
        
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"Meow Ma thuật đang bị nhiễu loạn Hệ thống báo lỗi: {str(e)}"

my_theme = gr.themes.Soft(
    primary_hue="fuchsia",
    secondary_hue="purple",
    neutral_hue="slate",
).set(
    body_text_color="#f8fafc",
    block_background_fill="rgba(15, 23, 42, 0.45)",
    block_border_color="#8b5cf6",
    block_border_width="1px",
    block_radius="xl",
    block_shadow="0 0 20px rgba(139, 92, 246, 0.15)",
    input_background_fill="rgba(30, 41, 59, 0.6)",
    button_primary_background_fill="#9333ea",
    button_primary_background_fill_hover="#a855f7",
)

custom_css = """
body {
    background: radial-gradient(circle at 50% -10%, #3b0764 0%, #05010f 80%) !important;
    background-attachment: fixed !important;
    margin: 0 !important;
    padding: 0 !important;
}
.glow-text {
    text-shadow: 0 0 10px #c084fc, 0 0 20px #a855f7;
}
.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
}
"""

with gr.Blocks(theme=my_theme, css=custom_css, fill_height=True) as demo:
    gr.Markdown("<h1 class='glow-text' style='text-align: center; color: #e9d5ff; font-weight: bold; font-size: 2em; margin-top: 15px; margin-bottom: 5px;'>✨ Lãnh Địa Ma Thuật của TƯ MÃ Ý 👹 và Siggy ✨</h1>")
    
    chatbot_ui = gr.Chatbot(
        avatar_images=[
            "https://link_anh_cua_ban.jpg",
            "https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg"
        ],
        scale=1
    )
    
    gr.ChatInterface(
        fn=chat_with_siggy,
        chatbot=chatbot_ui,
        fill_height=True,
        examples=["Ngươi là ai?", "TƯ MÃ Ý 👹 là ai đối với ngươi?", "Ritual là gì Infernet hoạt động ra sao?"]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
