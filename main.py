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
        return "Meow Ma thuật đang nhiễu loạn"

demo = gr.ChatInterface(
    fn=chat_with_siggy,
    title="Siggy The Soul Forge",
    description="Trò chuyện với thực thể đa chiều Siggy",
    examples=["Ngươi là ai", "Kể về BQDH đi"]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
