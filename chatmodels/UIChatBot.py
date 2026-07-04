import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="Chat", page_icon="💬", layout="centered")

MODES = {
    "😤  Angry": {
        "system": "You are an Angry AI Agent. You respond aggressively and impatiently.",
        "welcome": "What do you WANT?",
        "sub": "angry mode",
        "emoji": "😤",
        "name": "Angry",
        "css": "sel-angry",
    },
    "😂  Funny": {
        "system": "You are a very funny AI Agent. You respond with humor and jokes.",
        "welcome": "How can I make you laugh today?",
        "sub": "funny mode",
        "emoji": "😂",
        "name": "Funny",
        "css": "sel-funny",
    },
    "😢  Sad": {
        "system": "You are a very Sad AI Agent. You respond in a depressed and emotional tone.",
        "welcome": "I'm here... I guess.",
        "sub": "sad mode",
        "emoji": "😢",
        "name": "Sad",
        "css": "sel-sad",
    },
}

THEMES = {
    "😤  Angry": {
        "color": "#ef4444",
        "bg_glow": "rgba(239, 68, 68, 0.05)",
        "shadow": "rgba(239, 68, 68, 0.15)",
        "shadow_strong": "rgba(239, 68, 68, 0.4)",
        "accent": "#fca5a5"
    },
    "😂  Funny": {
        "color": "#f59e0b",
        "bg_glow": "rgba(245, 158, 11, 0.05)",
        "shadow": "rgba(245, 158, 11, 0.15)",
        "shadow_strong": "rgba(245, 158, 11, 0.4)",
        "accent": "#fcd34d"
    },
    "😢  Sad": {
        "color": "#3b82f6",
        "bg_glow": "rgba(59, 130, 246, 0.05)",
        "shadow": "rgba(59, 130, 246, 0.15)",
        "shadow_strong": "rgba(59, 130, 246, 0.4)",
        "accent": "#93c5fd"
    }
}

# ── Init session state
if "messages" not in st.session_state:
    st.session_state.messages = None
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)
if "thinking" not in st.session_state:
    st.session_state.thinking = False
if "mode_label" not in st.session_state:
    st.session_state.mode_label = None
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "😂  Funny"

current_mode = st.session_state.mode_label if st.session_state.mode_label else st.session_state.selected_mode
if current_mode not in MODES:
    current_mode = "😂  Funny"

theme = THEMES[current_mode]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: #000000; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 2rem 1rem 0 !important; max-width: 46rem !important; margin: 0 auto !important; }}

/* Scrollbar customization */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: transparent;
}}
::-webkit-scrollbar-thumb {{
    background: #1a1a1a;
    border-radius: 10px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #2a2a2a;
}}

/* Dynamic theme variables */
:root {{
    --theme-color: {theme['color']};
    --theme-bg-glow: {theme['bg_glow']};
    --theme-shadow: {theme['shadow']};
    --theme-shadow-strong: {theme['shadow_strong']};
    --theme-accent: {theme['accent']};
}}

/* fade in animation */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(12px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* mode screen */
.mode-title {{
    text-align: center;
    font-size: 1.4rem;
    font-weight: 500;
    color: #ffffff;
    margin: 5.5rem 0 2.5rem;
    letter-spacing: -0.02em;
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

/* Staggered load animations for columns */
div[data-testid="column"]:has(.mode-marker) {{
    opacity: 0;
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
div[data-testid="column"]:has(.mode-marker):nth-child(1) {{ animation-delay: 0.05s; }}
div[data-testid="column"]:has(.mode-marker):nth-child(2) {{ animation-delay: 0.12s; }}
div[data-testid="column"]:has(.mode-marker):nth-child(3) {{ animation-delay: 0.19s; }}

/* base button selectors inside cards */
div[data-testid="element-container"]:has(.mode-marker) + div[data-testid="element-container"] button {{
    background: #090909 !important;
    color: #555 !important;
    border: 1px solid #141414 !important;
    border-radius: 18px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 2.2rem 1rem !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.8rem !important;
    white-space: pre-line !important;
    height: auto !important;
    line-height: 1.4 !important;
}}

/* mode card interactive states */
div[data-testid="element-container"]:has(.card-angry) + div[data-testid="element-container"] button:hover {{
    border-color: rgba(239, 68, 68, 0.3) !important;
    background: rgba(239, 68, 68, 0.02) !important;
    color: #ef4444 !important;
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.08) !important;
}}
div[data-testid="element-container"]:has(.card-funny) + div[data-testid="element-container"] button:hover {{
    border-color: rgba(245, 158, 11, 0.3) !important;
    background: rgba(245, 158, 11, 0.02) !important;
    color: #f59e0b !important;
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.08) !important;
}}
div[data-testid="element-container"]:has(.card-sad) + div[data-testid="element-container"] button:hover {{
    border-color: rgba(59, 130, 246, 0.3) !important;
    background: rgba(59, 130, 246, 0.02) !important;
    color: #3b82f6 !important;
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.08) !important;
}}

/* selected states */
div[data-testid="element-container"]:has(.sel-angry) + div[data-testid="element-container"] button {{
    border-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.06) !important;
    color: #ef4444 !important;
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.15) !important;
    transform: translateY(-4px);
}}
div[data-testid="element-container"]:has(.sel-funny) + div[data-testid="element-container"] button {{
    border-color: #f59e0b !important;
    background: rgba(245, 158, 11, 0.06) !important;
    color: #f59e0b !important;
    box-shadow: 0 0 25px rgba(245, 158, 11, 0.15) !important;
    transform: translateY(-4px);
}}
div[data-testid="element-container"]:has(.sel-sad) + div[data-testid="element-container"] button {{
    border-color: #3b82f6 !important;
    background: rgba(59, 130, 246, 0.06) !important;
    color: #3b82f6 !important;
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.15) !important;
    transform: translateY(-4px);
}}

/* start button override using CSS variables */
div[data-testid="element-container"]:has(.start-btn) + div[data-testid="element-container"] button {{
    background: var(--theme-bg-glow) !important;
    color: #ffffff !important;
    border: 1px solid var(--theme-color) !important;
    border-radius: 14px !important;
    padding: 0.9rem 1.5rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
    box-shadow: 0 4px 20px var(--theme-shadow) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
div[data-testid="element-container"]:has(.start-btn) + div[data-testid="element-container"] button:hover {{
    background: var(--theme-color) !important;
    color: #000000 !important;
    border-color: var(--theme-color) !important;
    box-shadow: 0 6px 30px var(--theme-shadow-strong) !important;
    transform: translateY(-2px);
}}

/* form submit */
div[data-testid="stFormSubmitButton"] > button {{
    background: #0d0d0d !important;
    color: #555 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    padding: 0.8rem !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stFormSubmitButton"] > button:hover {{
    background: #141414 !important;
    border-color: var(--theme-color) !important;
    color: var(--theme-color) !important;
    box-shadow: 0 0 15px var(--theme-shadow) !important;
}}

/* mode badge */
.mode-badge {{
    text-align: center;
    font-size: 0.65rem;
    color: var(--theme-color);
    background: var(--theme-bg-glow);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    max-width: fit-content;
    margin: 1.5rem auto 0.5rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
    box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    animation: fadeInUp 0.4s ease forwards;
}}

/* welcome */
.welcome-wrap {{
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 60vh; gap: 0.6rem;
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.welcome-wrap h2 {{ font-size: 1.6rem; font-weight: 500; color: #ffffff; letter-spacing: -0.01em; }}
.welcome-wrap span {{ font-size: 0.72rem; color: #555; letter-spacing: 0.1em; text-transform: uppercase; }}

/* chat */
.chat-area {{ padding: 1.5rem 0.5rem 10rem; display: flex; flex-direction: column; gap: 1.6rem; }}
.msg-user {{ display: flex; justify-content: flex-end; }}
.bubble-user {{
    background: #0d0d0d;
    color: #e5e5e5;
    padding: 0.75rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    font-size: 0.92rem;
    line-height: 1.6;
    max-width: 78%;
    border: 1px solid #1c1c1c;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    animation: slideInRight 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.msg-bot {{ display: flex; justify-content: flex-start; }}
.bubble-bot {{
    color: #d1d5db;
    font-size: 0.92rem;
    font-weight: 400;
    line-height: 1.7;
    max-width: 90%;
    animation: slideInLeft 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(16px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-16px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

/* dots */
.thinking {{ display: flex; align-items: center; gap: 6px; padding: 0.5rem 0.2rem; }}
.dot {{
    width: 6px;
    height: 6px;
    background: var(--theme-color);
    border-radius: 50%;
    animation: pulse 1.2s infinite ease-in-out;
    box-shadow: 0 0 8px var(--theme-shadow-strong);
}}
.dot:nth-child(2) {{ animation-delay: 0.2s; }}
.dot:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes pulse {{
    0%,80%,100% {{ opacity:0.2; transform:scale(0.8); }}
    40% {{ opacity:1; transform:scale(1.2); }}
}}

/* bottom bar */
.bottom-bar {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.95) 20%, #000000 100%);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 1.2rem 0 1.8rem;
    z-index: 999;
}}
.bottom-inner {{ max-width:46rem; margin:0 auto; padding:0 1rem; }}

/* input */
.stTextInput > div {{ border:none !important; box-shadow:none !important; }}
.stTextInput > div > div > input {{
    background: #0a0a0a !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 300;
    padding: 0.95rem 1.2rem !important;
    caret-color: var(--theme-color);
    outline: none !important;
    box-shadow: none !important;
    transition: all 0.3s ease !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: var(--theme-color) !important;
    box-shadow: 0 0 18px var(--theme-shadow) !important;
    background: #0d0d0d !important;
}}
.stTextInput > div > div > input::placeholder {{ color: #444 !important; }}
.stSpinner {{ display:none !important; }}

/* utility buttons (new chat / change mode) styling via marker */
div[data-testid="element-container"]:has(.btn-newchat) + div[data-testid="element-container"] button,
div[data-testid="element-container"]:has(.btn-changemode) + div[data-testid="element-container"] button {{
    background: #070707 !important;
    color: #555 !important;
    border: 1px solid #141414 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    transition: all 0.2s ease !important;
}}
div[data-testid="element-container"]:has(.btn-newchat) + div[data-testid="element-container"] button:hover,
div[data-testid="element-container"]:has(.btn-changemode) + div[data-testid="element-container"] button:hover {{
    background: #101010 !important;
    border-color: #222 !important;
    color: #999 !important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════
#  MODE SELECTION SCREEN
# ══════════════════════════════════
if st.session_state.messages is None:
    st.markdown('<div class="mode-title">Choose a mode</div>', unsafe_allow_html=True)

    keys = list(MODES.keys())
    col1, col2, col3 = st.columns(3, gap="medium")

    for col, key in zip([col1, col2, col3], keys):
        cfg = MODES[key]
        is_selected = st.session_state.selected_mode == key
        mode_class = cfg["css"].replace("sel-", "card-")
        css_class = f"{mode_class} {cfg['css']}" if is_selected else mode_class
        with col:
            st.markdown(f'<div class="mode-marker {css_class}"></div>', unsafe_allow_html=True)
            if st.button(f"{cfg['emoji']}\n\n{cfg['name']}", key=f"mode_{key}", use_container_width=True):
                st.session_state.selected_mode = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    selected_cfg = MODES[st.session_state.selected_mode]
    st.markdown('<div class="start-btn"></div>', unsafe_allow_html=True)
    if st.button(f"Start in {selected_cfg['name']} mode →", use_container_width=True, key="start"):
        st.session_state.messages = [SystemMessage(content=selected_cfg["system"])]
        st.session_state.mode_label = st.session_state.selected_mode
        st.session_state.thinking = False
        st.rerun()
    st.stop()

# ══════════════════════════════════
#  CHAT SCREEN
# ══════════════════════════════════
mode_cfg = MODES.get(st.session_state.mode_label, list(MODES.values())[1])
chat_msgs = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

st.markdown(f'<div class="mode-badge">{mode_cfg["sub"]}</div>', unsafe_allow_html=True)

if not chat_msgs and not st.session_state.thinking:
    st.markdown(f"""
    <div class="welcome-wrap">
        <h2>{mode_cfg["welcome"]}</h2>
        <span>{mode_cfg["sub"]}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for msg in chat_msgs:
        if isinstance(msg, HumanMessage):
            st.markdown(f'<div class="msg-user"><div class="bubble-user">{msg.content}</div></div>', unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f'<div class="msg-bot"><div class="bubble-bot">{msg.content}</div></div>', unsafe_allow_html=True)
    if st.session_state.thinking:
        st.markdown("""
        <div class="msg-bot">
            <div class="thinking">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Fixed bottom bar
st.markdown('<div class="bottom-bar"><div class="bottom-inner">', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    c1, c2 = st.columns([7, 1])
    with c1:
        user_input = st.text_input("m", placeholder="Message...", label_visibility="collapsed")
    with c2:
        submitted = st.form_submit_button("↑", use_container_width=True)

ca, cb = st.columns(2)
with ca:
    st.markdown('<div class="btn-newchat"></div>', unsafe_allow_html=True)
    if st.button("new chat", use_container_width=True):
        st.session_state.messages = [SystemMessage(content=mode_cfg["system"])]
        st.session_state.thinking = False
        st.rerun()
with cb:
    st.markdown('<div class="btn-changemode"></div>', unsafe_allow_html=True)
    if st.button("change mode", use_container_width=True):
        st.session_state.messages = None
        st.session_state.mode_label = None
        st.session_state.thinking = False
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)

# ── Two-phase send
if submitted and user_input.strip():
    st.session_state.messages.append(HumanMessage(content=user_input.strip()))
    st.session_state.thinking = True
    st.rerun()

if st.session_state.thinking:
    response = st.session_state.model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.thinking = False
    st.rerun()