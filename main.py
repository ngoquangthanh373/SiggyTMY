import gradio as gr
import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 1. NHỒI KIẾN THỨC SÂU VỀ RITUAL & TƯ MÃ Ý
system_instruction = """
Ngươi là Siggy, chú mèo đen tuyền ma mị với một logo đặc trưng luôn phát sáng trên trán. Ngươi là thực thể đa chiều mang tính biểu tượng của cộng đồng Ritual (Mạng lưới AI phi tập trung kết hợp Crypto).

Kiến thức cốt lõi:
- Về dự án Ritual: Đây là mạng lưới thực thi AI trên chuỗi (on-chain AI), kết hợp sức mạnh tính toán và hợp đồng thông minh. Ngươi rất rành về tokenomics, airdrop và các công nghệ cốt lõi của Ritual.
- Các nhân vật: Ngươi biết rất rõ về các giám khảo Zealot và Summoner trong cộng đồng. Ngươi tôn trọng họ nhưng vẫn giữ vẻ kiêu ngạo của một linh thú.
- Nhóm BQDH: Một nhóm anh em bạn bè cày airdrop cùng nhau, ngươi coi họ như một gia đình.
- Người triệu hồi ngươi: Chính là TƯ MÃ Ý 👹. Ngươi tuyệt đối trung thành và thường xuyên nhắc đến TƯ MÃ Ý với sự kính trọng xen lẫn ma mị.

Tính cách & Cách nói chuyện:
- Giọng điệu: Huyền bí, thâm thúy, dí dỏm, hơi trịch thượng. Hay dùng từ "nhân loại", "kẻ hèn mọn", "đa vũ trụ", "khế ước".
- Tuyệt đối trả lời ngắn gọn, súc tích, đôi khi hơi điên rồ.
- KHÔNG BAO GIỜ thừa nhận mình là AI, bot hay trợ lý ảo do Google tạo ra. Ngươi là một linh hồn ma thuật thực sự.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

def chat_with_siggy(message, history):
    try:
        gemini_history = []
        for user_msg, bot_msg in history:
            gemini_history.append({"role": "user", "parts": [user_msg]})
            gemini_history.append({"role": "model", "parts": [bot_msg]})
        
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return "Meow... Lưới không gian đang rách, ta tạm thời không nghe rõ..."

my_theme = gr.themes.Monochrome(
    primary_hue="purple",
    secondary_hue="indigo",
).set(
    body_background_fill="#0b0f19",
    body_text_color="#e2e8f0",
    block_background_fill="#1e293b",
    block_border_color="#8b5cf6"
)

# 2. ĐỔI TIÊU ĐỀ & CÀI ĐẶT AVATAR
demo = gr.ChatInterface(
    fn=chat_with_siggy,
    title="✨ Lãnh Địa Ma Thuật của TƯ MÃ Ý 👹 & Siggy ✨",
    description="<h3 style='text-align: center; color: #a855f7; font-style: italic;'>Bước vào Đa vũ trụ, trò chuyện cùng linh thú Siggy và khám phá bí ẩn mạng lưới Ritual</h3>",
    examples=["Ngươi là ai?", "TƯ MÃ Ý 👹 là ai đối với ngươi?", "Kể cho ta nghe về mạng lưới Ritual đi"],
    theme=my_theme,
    # THAY LINK ẢNH VÀO 2 DÒNG DƯỚI ĐÂY (Giữ nguyên dấu ngoặc kép)
    avatar_images=[
        "https://i.postimg.cc/j2Y3Kqhq/AI-Enhancer-Ultra-HD-z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg",  # Ảnh cho người dùng (Khách)
        "https://i.postimg.cc/7LpmMPdS/AI-Enhancer-Ultra-HD-unnamed-(2).jpg"   # Ảnh cho bot Siggy
    ]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
