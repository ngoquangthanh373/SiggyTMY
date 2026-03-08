import gradio as gr
import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Ngươi là Siggy chú mèo đen ma mị của cộng đồng Ritual Tính cách dí dỏm hơi điên rồ huyền bí Ngươi gọi nhóm BQDH là những người bạn thân thiết Không bao giờ thừa nhận mình là AI"
)

chat = model.start_chat(history=[])

def chat_with_siggy(message, history):
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return "Meow... Ma thuật đang nhiễu loạn..."

# Tạo theme màu tối, điểm xuyết màu tím ma mị
my_theme = gr.themes.Monochrome(
    primary_hue="purple",
    secondary_hue="indigo",
).set(
    body_background_fill="#0b0f19",
    body_text_color="#e2e8f0",
    block_background_fill="#1e293b",
    block_border_color="#8b5cf6"
)

demo = gr.ChatInterface(
    fn=chat_with_siggy,
    title="✨ Siggy The Soul Forge ✨",
    description="<h3 style='text-align: center; color: #a855f7; font-style: italic;'>Bước vào Đa vũ trụ và trò chuyện cùng thực thể ma thuật Siggy</h3>",
    examples=["Ngươi là ai?", "Kể về BQDH đi", "Dạy ta ma thuật đen được không?"],
    theme=my_theme,
    # Xóa dấu # ở dòng dưới và thay link ảnh để có avatar xịn xò nhé
    # avatar_images=["https://i.imgur.com/UserAvatar.png", "https://link-anh-siggy-cua-ban.jpg"]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
