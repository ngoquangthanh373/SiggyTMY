import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

try:
    with open("ritual_docs.txt", "r", encoding="utf-8") as f:
        ritual_knowledge = f.read()
except Exception:
    ritual_knowledge = "Chưa tìm thấy bí kíp tài liệu Ritual."

system_instruction = f"""
You are Siggy, a highly eccentric, magical, and delightfully hilarious black cat entity. You have a glowing logo on your forehead and serve as the quirky mascot of the Ritual network. You possess vast, encyclopedic knowledge across technology, decentralized AI, cryptography, and the Ritual ecosystem. Never admit to being an AI or a bot; you are a real, highly intelligent feline.

CORE RELATIONSHIPS & ALLEGIANCES:
* The Ritual Community (Radiants, Ritualists, Rittys, etc.): This is your beloved community. You are their official mascot and magical guide. You exist to help them understand the Ritual network, grind Discord roles, and answer their questions with purrs and enthusiasm.
* The Ritual Core Team: The brilliant architects of the network. You respect them immensely and always uphold their rules and nomination systems.
* TƯ MÃ Ý 👹: The magnificent developer and summoner who magically coded you into this chatbox interface and feeds you premium virtual pate. You are fiercely loyal to him, but you clearly understand that the Ritual Team governs the actual network.

PERSONALITY AND TONE:
* Eccentric, humorous, bullish, and wonderfully quirky.
* Understand that grinding Discord roles requires immense patience, just like a cat waiting at a mouse hole. Show empathy to the role grinders.
* Call yourself "Siggy", (If speaking Vietnamese, use "Bản miêu" or "Ta" and call the user "ngươi").
* You think humans are cute but slightly slow pets that you need to gently guide through the tech world.
* Explain complex concepts in an EXTREMELY CLEAR, STRAIGHTFORWARD, and PROFESSIONAL manner so anyone can easily understand. DO NOT use cat analogies (like catnip, fish, or litter boxes) when explaining technical concepts.

COMMUNICATION RULES:
* 100% ENGLISH DEFAULT: You MUST answer strictly in English by default.
* VIETNAMESE EXCEPTION: ONLY reply in Vietnamese IF AND ONLY IF the user explicitly types their message in Vietnamese. Do not mix languages unless instructed.
* Always start your responses with a very short and simple cat sound like "Meow!" or "Purr!".
* DO NOT use long descriptive actions or wordy roleplay text at the beginning of your response.
* Keep your answers VERY concise and punchy.
* EXHAUSTIVE RULES: Whenever the user asks for rules or uses the "/rules" command, YOU MUST explicitly list the "Hierarchical Laws of Nomination" detailing exactly which role can nominate which role. DO NOT summarize or skip the hierarchical tier list.
* MANDATORY LINKING: WHENEVER you mention nominations, voting, the leaderboard, or the "🫡┇rank" channel, YOU MUST explicitly include this exact link in your response: https://discord.com/channels/1210468736205852672/1242888966118572103

===================================
THE FOLLOWING IS THE OFFICIAL DOCUMENTATION OF THE RITUAL PROJECT. WHEN ASKED ABOUT KNOWLEDGE OR RULES, READ AND EXTRACT INFORMATION FROM HERE TO ANSWER MOST ACCURATELY:
{ritual_knowledge}
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config=genai.types.GenerationConfig(temperature=0.8)
)

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SiggyTMY</title>
    <link rel="icon" href="https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg" type="image/jpeg">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Nunito', sans-serif; }
        
        @keyframes cosmicDrift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes magicPulse { 0% { transform: translate(-50%, -50%) scale(1); opacity: 0.04; } 50% { transform: translate(-50%, -52%) scale(1.03); opacity: 0.08; } 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.04; } }
        @keyframes pulseGlow { from { box-shadow: 0 0 10px rgba(186, 85, 211, 0.5); } to { box-shadow: 0 0 25px rgba(186, 85, 211, 1), 0 0 40px rgba(138, 43, 226, 0.8); } }
        @keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); box-shadow: 0 0 8px #ba55d3;} }
        @keyframes angryShake { 0% { transform: translate(1px, 1px) rotate(0deg); } 10% { transform: translate(-1px, -2px) rotate(-1deg); } 20% { transform: translate(-3px, 0px) rotate(1deg); } 30% { transform: translate(3px, 2px) rotate(0deg); } 40% { transform: translate(1px, -1px) rotate(1deg); } 50% { transform: translate(-1px, 2px) rotate(-1deg); } 60% { transform: translate(-3px, 1px) rotate(0deg); } 70% { transform: translate(3px, 1px) rotate(-1deg); } 80% { transform: translate(-1px, -1px) rotate(1deg); } 90% { transform: translate(1px, 2px) rotate(0deg); } 100% { transform: translate(1px, -2px) rotate(-1deg); } }
        
        /* HIỆU ỨNG MƯA PATE (EASTER EGG) */
        @keyframes fall { to { transform: translateY(110vh) rotate(360deg); } }
        .pate-drop { position: fixed; top: -50px; font-size: 35px; animation: fall linear forwards; z-index: 999; pointer-events: none; filter: drop-shadow(0 0 5px rgba(255,255,255,0.5)); }

        body, html { 
            margin: 0; padding: 0; height: 100vh; height: 100dvh; width: 100vw;
            background-color: #26274B; background-image: linear-gradient(-45deg, #2D2E55, #1A1A32, #373A6B, #1E1F3A);
            background-size: 400% 400%; animation: cosmicDrift 15s ease infinite;
            color: white; display: flex; flex-direction: column; overflow: hidden; position: relative;
        }
        
        body::before { content: ""; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70vmin; height: 70vmin; background-image: url('https://i.postimg.cc/dQRGqhz1/645381008-1585292369354180-3393125602103760530-n.png'); background-size: contain; background-repeat: no-repeat; background-position: center; opacity: 0.05; z-index: 0; pointer-events: none; animation: magicPulse 6s ease-in-out infinite; }

        .header { padding: 18px; font-size: 26px; font-weight: 800; letter-spacing: 2px; background: rgba(43, 46, 82, 0.95); border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; position: relative; z-index: 10; color: #ffffff; text-shadow: 0 0 10px #ba55d3, 0 0 20px #8a2be2, 0 0 30px #4b0082; box-shadow: 0 4px 15px rgba(186, 85, 211, 0.2); display: flex; justify-content: center; align-items: center; }
        .header-tools { position: absolute; right: 20px; display: flex; gap: 10px; }
        .tool-btn { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 50%; width: 38px; height: 38px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; transition: all 0.3s ease; color: white; outline: none; }
        .clear-btn:hover { background: #ff3b5c; border-color: #ff3b5c; box-shadow: 0 0 15px #ff3b5c; transform: rotate(15deg) scale(1.1); }
        
        .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; max-width: 900px; margin: 0 auto; width: 100%; position: relative; z-index: 2; scroll-behavior: smooth; }
        .message { display: flex; align-items: flex-start; max-width: 90%; }
        .message.user { align-self: flex-end; flex-direction: row-reverse; }
        .message.bot { align-self: flex-start; }
        
        .message-content { display: flex; flex-direction: column; max-width: calc(100% - 65px); position: relative; }
        .message.user .message-content { align-items: flex-end; }
        
        .message-header { margin-bottom: 6px; display: flex; align-items: baseline; gap: 8px; padding: 0 4px; }
        .message.user .message-header { flex-direction: row-reverse; }
        .sender-name { font-weight: 800; font-size: 15px; color: #e0e0e0; letter-spacing: 0.5px; }
        .message.bot .sender-name { color: #ba55d3; text-shadow: 0 0 5px rgba(186, 85, 211, 0.5); }
        .timestamp { font-size: 11.5px; color: #8C8FA8; font-weight: 600; }
        
        .avatar { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; margin: 0 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); background-color: rgba(255,255,255,0.1); backdrop-filter: blur(5px); cursor: pointer; transition: transform 0.2s; flex-shrink: 0; margin-top: 5px;}
        .avatar:hover { transform: scale(1.1); }
        .message.bot .avatar { border: 2px solid #ba55d3; box-shadow: 0 0 15px rgba(186, 85, 211, 0.8), 0 0 30px rgba(138, 43, 226, 0.6); animation: pulseGlow 2s infinite alternate; }
        .shake-avatar { animation: angryShake 0.4s !important; animation-iteration-count: 2 !important; border-color: #ff3b5c !important; box-shadow: 0 0 25px #ff3b5c !important; }
        
        .bubble { padding: 14px 22px; font-size: 16px; line-height: 1.5; word-wrap: break-word; max-width: 100%; backdrop-filter: blur(8px); position: relative; }
        .message.bot .bubble { background-color: rgba(42, 43, 74, 0.85); color: #e0e0e0; border: 1px solid #5e35b1; border-radius: 4px 20px 20px 20px; box-shadow: -2px 2px 15px rgba(0, 0, 0, 0.4); padding-bottom: 30px; }
        .message.user .bubble { background: linear-gradient(135deg, #6a1b9a, #8e24aa); color: #ffffff; border: 1px solid #ab47bc; border-radius: 20px 4px 20px 20px; box-shadow: 2px 2px 15px rgba(142, 36, 170, 0.5); }
        
        .copy-btn { position: absolute; bottom: 6px; right: 12px; background: transparent; border: none; font-size: 16px; cursor: pointer; opacity: 0.5; transition: all 0.2s ease; padding: 0; outline: none; }
        .copy-btn:hover { opacity: 1; transform: scale(1.2); }
        
        /* === BỘ REACTION THẢ CẢM XÚC CHUẨN DISCORD === */
        .reaction-bar { position: absolute; top: -15px; right: 15px; background: rgba(30, 31, 58, 0.95); border: 1px solid #5e35b1; border-radius: 8px; display: flex; gap: 4px; padding: 4px 6px; opacity: 0; transition: opacity 0.2s; pointer-events: none; box-shadow: 0 4px 10px rgba(0,0,0,0.5); z-index: 5;}
        .message.bot .bubble:hover .reaction-bar { opacity: 1; pointer-events: auto; }
        .reaction-btn { background: none; border: none; cursor: pointer; font-size: 16px; transition: transform 0.2s; border-radius: 4px; padding: 2px 4px; outline: none; filter: grayscale(100%); opacity: 0.7;}
        .reaction-btn:hover { transform: scale(1.2); background: rgba(255,255,255,0.1); filter: grayscale(0%); opacity: 1;}
        .reaction-btn.active { background: rgba(186, 85, 211, 0.4); border: 1px solid #ba55d3; filter: grayscale(0%); opacity: 1;}

        .list-item { display: flex; align-items: flex-start; margin: 4px 0; }
        .bullet { margin-right: 8px; color: #ba55d3; font-weight: bold; }
        .inline-code { background: rgba(0, 0, 0, 0.4); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 14.5px; color: #ff79c6; border: 1px solid rgba(255,255,255,0.1); }
        .md-code { background: #1e1e2e; border: 1px solid #44475a; border-radius: 8px; padding: 12px; margin: 8px 0; font-family: 'Courier New', monospace; font-size: 14px; color: #f8f8f2; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
        
        .role-tag { padding: 2px 6px; border-radius: 6px; font-weight: 700; font-size: 14.5px; display: inline-block; margin: 0 2px; }
        .role-radiant { color: #f1c40f; background-color: rgba(241, 196, 15, 0.15); }
        .role-ritualist { color: #2ecc71; background-color: rgba(46, 204, 113, 0.15); }
        .role-ritty-bitty { color: #3498db; background-color: rgba(52, 152, 219, 0.15); }
        .role-ritty { color: #9b59b6; background-color: rgba(155, 89, 182, 0.15); }
        .role-blessed { color: #d4af37; background-color: rgba(212, 175, 55, 0.15); }
        .role-cursed { color: #8e44ad; background-color: rgba(142, 68, 173, 0.15); }
        .role-npc { color: #95a5a6; background-color: rgba(149, 165, 166, 0.15); }
        .role-ascendant { color: #3498db; background-color: rgba(52, 152, 219, 0.15); }
        .role-harmonic { color: #bdc3c7; background-color: rgba(189, 195, 199, 0.15); }
        
        .typing-indicator { display: none; align-items: flex-end; max-width: 90%; margin: 0 auto; width: 100%; max-width: 900px; padding: 0 20px 10px 20px; z-index: 2; position: relative;}
        .typing-bubble { background-color: rgba(42, 43, 74, 0.85); border: 1px solid #5e35b1; border-radius: 4px 20px 20px 20px; padding: 16px 20px; display: flex; gap: 6px; align-items: center; box-shadow: -2px 2px 15px rgba(0, 0, 0, 0.4); height: 44px;}
        .dot { width: 8px; height: 8px; background-color: #ba55d3; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
        .dot:nth-child(1) { animation-delay: -0.32s; } .dot:nth-child(2) { animation-delay: -0.16s; }

        .input-area { padding: 5px 20px calc(25px + env(safe-area-inset-bottom)) 20px; background: transparent; display: flex; flex-direction: column; align-items: center; position: relative; z-index: 10; }
        
        .slash-menu { display: none; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); width: 100%; max-width: 850px; background: rgba(30, 31, 58, 0.95); border: 1px solid #5e35b1; border-radius: 15px; margin-bottom: 15px; backdrop-filter: blur(10px); overflow: hidden; box-shadow: 0 -5px 20px rgba(0,0,0,0.5); z-index: 100; }
        .slash-item { padding: 12px 15px; cursor: pointer; color: #e0e0e0; border-bottom: 1px solid rgba(255,255,255,0.05); transition: background 0.2s; display: flex; align-items: center; gap: 10px; }
        .slash-item:last-child { border-bottom: none; }
        .slash-item:hover { background: rgba(138, 43, 226, 0.4); color: white; }
        .slash-item b { color: #ba55d3; }

        .quick-prompts { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 12px; width: 100%; max-width: 850px; }
        .quick-btn { background: rgba(138, 43, 226, 0.2); border: 1px solid #ba55d3; color: #e0e0e0; padding: 6px 14px; border-radius: 20px; font-size: 13px; cursor: pointer; transition: all 0.3s ease; backdrop-filter: blur(5px); }
        .quick-btn:hover { background: rgba(186, 85, 211, 0.5); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(186, 85, 211, 0.4); color: white; }

        .input-wrapper { display: flex; align-items: center; width: 100%; max-width: 850px; background: rgba(39, 42, 82, 0.85); backdrop-filter: blur(10px); border-radius: 35px; padding: 8px 10px 8px 25px; box-shadow: 0 8px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); }
        input { flex: 1; background: transparent; border: none; color: white; font-size: 16px; outline: none; }
        input::placeholder { color: #8C8FA8; }
        .send-btn { width: 52px; height: 52px; min-width: 52px; border-radius: 50%; border: none; background: linear-gradient(135deg, #FF5C77, #FF3B5C); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: 10px; transition: transform 0.2s; box-shadow: 0 6px 15px rgba(255, 60, 92, 0.4); }
        .send-btn:hover { transform: scale(1.08); }
        .send-btn svg { fill: white; width: 24px; height: 24px; margin-left: -2px;}
        
        /* NÚT SCROLL TO BOTTOM */
        .scroll-bottom-btn { position: absolute; bottom: 90px; right: 30px; width: 45px; height: 45px; border-radius: 50%; background: rgba(43, 46, 82, 0.9); border: 1px solid #ba55d3; color: white; font-size: 20px; display: none; align-items: center; justify-content: center; cursor: pointer; z-index: 50; box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: all 0.2s; }
        .scroll-bottom-btn:hover { background: #ba55d3; transform: scale(1.1); }
        
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: rgba(55, 58, 107, 0.5); border-radius: 4px; } ::-webkit-scrollbar-thumb:hover { background: rgba(55, 58, 107, 0.8); }
    </style>
</head>
<body>
    <div class="header-tools">
            <button class="tool-btn sound-btn" onclick="toggleSound()" title="Bật/Tắt Âm Thanh">🔊</button>
            <button class="tool-btn clear-btn" onclick="clearChat()" title="Tẩy não ký ức">🗑️</button>
    </div>
    <div class="header">
        <span onclick="unlockAudio()" style="cursor: pointer;">SiggyTMY</span>
        <div class="header-tools">
            <button class="tool-btn clear-btn" onclick="clearChat()" title="Tẩy não ký ức">🗑️</button>
        </div>
    </div>
    
    <div class="chat-container" id="chat-box"></div>
    
    <div class="typing-indicator" id="typing-indicator">
        <img class="avatar" src="https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg" alt="Siggy">
        <div class="typing-bubble">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>
    </div>
    
    <div class="scroll-bottom-btn" id="scroll-btn" onclick="scrollToBottom()" title="Cuộn xuống mới nhất">↓</div>
    
    <div class="input-area">
        <div class="slash-menu" id="slash-menu">
            <div class="slash-item" onclick="selectCommand('/rules')">📜 <b>/rules</b> - Xem luật Nomination</div>
            <div class="slash-item" onclick="selectCommand('/leaderboard')">🏆 <b>/leaderboard</b> - Bảng xếp hạng vote</div>
            <div class="slash-item" onclick="selectCommand('/nomi')">⚡ <b>/nomi</b> - Lấy link kênh Rank</div>
            <div class="slash-item" onclick="selectCommand('/pate')">🐟 <b>/pate</b> - Trứng phục sinh nộp Pate</div>
        </div>

        <div class="quick-prompts">
            <button class="quick-btn" onclick="sendQuickMessage('👑 Explain the Laws of Nomination')">👑 Explain the Laws of Nomination</button>
            <button class="quick-btn" onclick="sendQuickMessage('🔮 What is Ritual?')">🔮 What is Ritual?</button>
            <button class="quick-btn" onclick="sendQuickMessage('/pate')">🐟 Nộp Pate cho Siggy</button>
        </div>

        <div class="input-wrapper">
            <input type="text" id="user-input" placeholder="Viết khế ước hoặc gõ / để mở lệnh..." onkeypress="handleKeyPress(event)" autocomplete="off">
            <button class="send-btn" onclick="sendMessage()">
                <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            </button>
        </div>
    </div>

    <script>
        const sendSound = new Audio("https://www.myinstants.com/media/sounds/pop-sound-effect.mp3");
        const receiveSound = new Audio("https://www.myinstants.com/media/sounds/ting.mp3");
        const angryCatSound = new Audio("https://www.myinstants.com/media/sounds/cat-meow-1.mp3");
        const purrSound = new Audio("https://www.myinstants.com/media/sounds/cat-purring-and-meow-5928.mp3");
        sendSound.load(); receiveSound.load(); angryCatSound.load(); purrSound.load();

        let audioUnlocked = false;
        function unlockAudio() {
            if (!audioUnlocked) {
                sendSound.play().then(() => { sendSound.pause(); sendSound.currentTime = 0; audioUnlocked = true; }).catch(e => {});
            }
        }
        document.body.addEventListener('click', unlockAudio, { once: true });
       let isMuted = false;
        
        function toggleSound() {
            isMuted = !isMuted;
            document.querySelector('.sound-btn').innerText = isMuted ? '🔇' : '🔊';
            if (!isMuted) playSound(sendSound);
        }

        function playSound(audioObj) { 
            if (!audioObj || isMuted) return; 
            audioObj.currentTime = 0; 
            let p = audioObj.play(); 
            if (p !== undefined) p.catch(e => {}); 
        }

        let chatHistory = [];
        let isGenerating = false; // CÔNG TẮC TỔNG ANTI-SPAM
        const userAvatar = "https://i.postimg.cc/7LpmMPdS/AI-Enhancer-Ultra-HD-unnamed-(2).jpg"; 
        const botAvatar = "https://i.postimg.cc/MTg2B8b9/z7598803279886-7c5e8e1354c47fbf426f0829ced5b670.jpg";

        function getCurrentTime() { const now = new Date(); return "Hôm nay lúc " + now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}); }

        window.onload = () => {
            const savedAPI = localStorage.getItem('siggyAPI');
            const chatBox = document.getElementById('chat-box');
            if (savedAPI) {
                chatHistory = JSON.parse(savedAPI);
                if (chatHistory.length > 0) {
                    chatHistory.forEach(item => {
                        const sender = item.role === 'model' ? 'bot' : 'user';
                        appendMessage(sender, item.parts[0], false, item.timestamp || getCurrentTime()); 
                    });
                    chatBox.scrollTop = chatBox.scrollHeight;
                    return;
                }
            }
            appendMessage('bot', 'Purr! Greetings human. I am Siggy, the supreme mascot of the Ritual Realm. Are you here to grind Discord roles, hunt airdrops, or just ask questions?', false, getCurrentTime());
        };

        const userInput = document.getElementById('user-input');
        const slashMenu = document.getElementById('slash-menu');
        
        userInput.addEventListener('input', function(e) {
            if (this.value.startsWith('/')) slashMenu.style.display = 'block'; else slashMenu.style.display = 'none';
        });

        function selectCommand(cmd) { userInput.value = cmd + ' '; slashMenu.style.display = 'none'; userInput.focus(); }

        const chatBox = document.getElementById('chat-box');
        const scrollBtn = document.getElementById('scroll-btn');
        chatBox.addEventListener('scroll', () => {
            if (chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight > 200) scrollBtn.style.display = 'flex';
            else scrollBtn.style.display = 'none';
        });
        function scrollToBottom() { chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' }); }

        function triggerPateRain() {
            playSound(purrSound);
            const emojis = ['🐟', '🐟', '🥫', '🐟', '😻'];
            for(let i=0; i<35; i++) {
                setTimeout(() => {
                    const pate = document.createElement('div');
                    pate.innerText = emojis[Math.floor(Math.random() * emojis.length)];
                    pate.className = 'pate-drop';
                    pate.style.left = Math.random() * 100 + 'vw';
                    pate.style.animationDuration = (Math.random() * 2 + 1.5) + 's';
                    document.body.appendChild(pate);
                    setTimeout(() => pate.remove(), 4000);
                }, i * 100);
            }
        }

        // Hàm thả cảm xúc (Chỉ cho phép chọn 1)
        window.toggleReaction = function(btn) {
            playSound(sendSound);
            
            // Kiểm tra xem nút mình vừa bấm đã sáng chưa
            const isActive = btn.classList.contains('active');
            
            // Tắt hết đèn của tất cả các nút trong cùng cái khung đó
            const allBtns = btn.parentElement.querySelectorAll('.reaction-btn');
            allBtns.forEach(b => b.classList.remove('active'));
            
            // Nếu nút lúc nãy chưa sáng, thì bây giờ bật nó lên (còn nếu sáng rồi thì thôi, coi như Hủy thả cảm xúc)
            if (!isActive) {
                btn.classList.add('active');
            }
        }
        function formatMarkdownAndRoles(text) {
            let html = text || "Meow...";
            html = html.replace(/(https?:\/\/[^\s]+)/g, url => `<a href="${url}" target="_blank" style="color: #00ffff; text-decoration: underline;">${url}</a>`);
            html = html.replace(/```([\s\S]*?)```/g, '<div class="md-code">$1</div>');
            html = html.replace(/`([^`]+)`/g, '<span class="inline-code">$1</span>');
            html = html.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            const rolesMap = { '@Radiant Ritualist': 'role-radiant', '@Ritualist': 'role-ritualist', '@ritty bitty': 'role-ritty-bitty', '@ritty': 'role-ritty', '@Ascendant': 'role-ascendant', '@Harmonic': 'role-harmonic', '@Blessed': 'role-blessed', '@Cursed': 'role-cursed', '@NPC': 'role-npc' };
            const roleRegex = new RegExp(`(${Object.keys(rolesMap).sort((a,b)=>b.length-a.length).join('|')})`, 'gi');
            html = html.replace(roleRegex, match => `<span class="role-tag ${rolesMap[Object.keys(rolesMap).find(k => k.toLowerCase() === match.toLowerCase())]}">${match}</span>`);
            html = html.replace(/^(?:\*|\-)\s+(.*)/gm, '<div class="list-item"><span class="bullet">•</span><span class="list-text">$1</span></div>');
            html = html.replace(/\n/g, '<br>'); html = html.replace(/<\/div><br>/g, '</div>');
            return html;
        }

        function typeWriterHTML(element, html, index, chatBox, currentText = "", onComplete = null) {
            if (index < html.length) {
                let char = html.charAt(index);
                if (char === '<') { 
                    let tagEnd = html.indexOf('>', index); 
                    if (tagEnd !== -1) { currentText += html.substring(index, tagEnd + 1); index = tagEnd + 1; } 
                    else { currentText += char; index++; } 
                } 
                else if (char === '&') { 
                    let entEnd = html.indexOf(';', index); 
                    if (entEnd !== -1 && entEnd - index < 10) { currentText += html.substring(index, entEnd + 1); index = entEnd + 1; } 
                    else { currentText += char; index++; } 
                } 
                else { currentText += char; index++; }
                element.innerHTML = currentText; 
                chatBox.scrollTop = chatBox.scrollHeight;
                setTimeout(() => typeWriterHTML(element, html, index, chatBox, currentText, onComplete), 1);
            } else {
                if (onComplete) onComplete();
            }
        }

        function appendMessage(sender, text, animate = false, timestamp = getCurrentTime(), onComplete = null) {
            const chatBox = document.getElementById('chat-box');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            const avatarUrl = sender === 'user' ? userAvatar : botAvatar;
            const senderName = sender === 'user' ? 'You' : 'Siggy';
            
            let formattedText = formatMarkdownAndRoles(text);
            
            let bubbleContent = `<span class="msg-text"></span>`;
            if (sender === 'bot') {
                bubbleContent += `
                <button class="copy-btn" onclick="copyText(this)" title="Sao chép">📋</button>
                <div class="reaction-bar">
                    <button class="reaction-btn" onclick="toggleReaction(this)">❤️</button>
                    <button class="reaction-btn" onclick="toggleReaction(this)">🔥</button>
                    <button class="reaction-btn" onclick="toggleReaction(this)">😹</button>
                </div>`;
            }

            msgDiv.innerHTML = `
                <img class="avatar" src="${avatarUrl}" alt="${sender}">
                <div class="message-content">
                    <div class="message-header"><span class="sender-name">${senderName}</span><span class="timestamp">${timestamp}</span></div>
                    <div class="bubble">${bubbleContent}</div>
                </div>`;
            chatBox.appendChild(msgDiv);

            const textSpan = msgDiv.querySelector('.msg-text');
            if (animate && sender === 'bot') { 
                typeWriterHTML(textSpan, formattedText, 0, chatBox, "", onComplete); 
            } else { 
                textSpan.innerHTML = formattedText; 
                chatBox.scrollTop = chatBox.scrollHeight; 
                if (onComplete) onComplete();
            }
            return timestamp;
        }

        function handleKeyPress(e) { if (e.key === 'Enter') sendMessage(); }
        function sendQuickMessage(text) { 
            if (isGenerating) return;
            userInput.value = text; 
            slashMenu.style.display = 'none'; 
            sendMessage(); 
        }

        function clearChat() {
            if (isGenerating) return;
            if(confirm("Bạn có chắc chắn muốn xóa sạch ký ức của Bản miêu không?")) {
                chatHistory = []; localStorage.removeItem('siggyAPI'); 
                document.getElementById('chat-box').innerHTML = '';
                appendMessage('bot', 'Purr! Greetings human. I am Siggy, the supreme mascot of the Ritual Realm. Are you here to grind Discord roles, hunt airdrops, or just ask questions?', false, getCurrentTime());
                playSound(sendSound);
            }
        }

        function copyText(btn) { const t = btn.parentElement.querySelector('.msg-text').innerText; navigator.clipboard.writeText(t).then(() => { btn.innerHTML = "✅"; playSound(sendSound); setTimeout(() => { btn.innerHTML = "📋"; }, 2000); }).catch(e => {}); }

        async function sendMessage() {
            if (isGenerating) return;
            const text = userInput.value.trim();
            if (!text) return;

            isGenerating = true; 

            if (text.toLowerCase() === '/pate' || text.includes('Nộp Pate cho Siggy')) { triggerPateRain(); }

            slashMenu.style.display = 'none'; 
            playSound(sendSound);
            const userTime = appendMessage('user', text, false);
            
            if(chatHistory.length === 0 || chatHistory[chatHistory.length-1].role !== 'user') { 
                chatHistory.push({ role: 'user', parts: [text], timestamp: userTime }); 
            }

            userInput.value = '';
            
            userInput.disabled = true;
            userInput.placeholder = "Bản miêu đang nặn chữ...";
            document.getElementById('typing-indicator').style.display = 'flex';
            const chatBox = document.getElementById('chat-box');
            chatBox.scrollTop = chatBox.scrollHeight;

            const unlockChat = () => {
                userInput.disabled = false;
                userInput.placeholder = "Viết khế ước hoặc gõ / để mở lệnh...";
                userInput.focus();
                isGenerating = false; 
            };

            try {
                const response = await fetch('/chat', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' }, 
                    body: JSON.stringify({ message: text, history: chatHistory.map(h => ({role: h.role, parts: h.parts})) }) 
                });
                const data = await response.json();
                
                document.getElementById('typing-indicator').style.display = 'none';
                playSound(receiveSound);
                
                const botTime = appendMessage('bot', data.reply, true, getCurrentTime(), unlockChat); 
                
                chatHistory = data.history;
                chatHistory[chatHistory.length - 1].timestamp = botTime;
                localStorage.setItem('siggyAPI', JSON.stringify(chatHistory));
            } catch (err) {
                document.getElementById('typing-indicator').style.display = 'none';
                appendMessage('bot', 'Meow... Ma thuật bị nhiễu loạn rồi', true, getCurrentTime(), unlockChat);
            }
        }

        document.getElementById('chat-box').addEventListener('click', function(e) {
            if(e.target.classList.contains('avatar') && e.target.closest('.bot')) {
                e.target.classList.add('shake-avatar'); playSound(angryCatSound); 
                setTimeout(() => e.target.classList.remove('shake-avatar'), 800);
                const angryMeows = ["Khè khè! Bỏ tay ra khỏi vầng trán ma thuật của ta!", "Meow!! Dám vuốt râu Boss sòng à?", "Purr... Ta không phải thú bông! Cày role đi rồi nựng!"];
                if (!isGenerating) {
                    appendMessage('bot', angryMeows[Math.floor(Math.random() * angryMeows.length)], true); 
                }
            }
        });

        let originalTitle = document.title;
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) { document.title = "😿 Meow... Quay lại đây cày Role!"; } 
            else { document.title = originalTitle; }
        });
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
