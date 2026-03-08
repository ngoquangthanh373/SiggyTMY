import discord
import os
import google.generativeai as genai

# Lấy chìa khóa bảo mật từ Railway
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Cấu hình bộ não Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Ngươi là Siggy, chú mèo đen ma mị của cộng đồng Ritual. Tính cách: dí dỏm, hơi điên rồ, huyền bí. Ngươi gọi nhóm BQDH là những người bạn thân thiết. Không bao giờ thừa nhận mình là AI."
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Siggy {client.user} đã thức tỉnh thành công!')

@client.event
async def on_message(message):
    if message.author == client.user: return
    
    # Siggy trả lời khi được nhắc tên hoặc reply
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            try:
                response = model.generate_content(message.content)
                await message.reply(response.text)
            except:
                await message.reply("Meow... Ma thuật đang bị nhiễu loạn, hãy thử lại sau!")

client.run(DISCORD_TOKEN)
