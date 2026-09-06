import streamlit as st
import time
import json
import os
if not hasattr(st, 'cache'):
    st.cache = st.cache_resource
    
from streamlit_cookies_manager import EncryptedCookieManager
import uuid

cookies = EncryptedCookieManager(
    prefix="mychatapp_",
    password=os.environ.get("COOKIE_PASSWORD", "default_fallback_password")
)
if not cookies.ready():
    st.stop()

if "user_id" not in cookies or not cookies["user_id"]:
    cookies["user_id"] = str(uuid.uuid4())
    cookies.save()

user_id = cookies["user_id"]
try:
    with open("chats.json", "r") as f:
        full_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    full_data = {}

all_chats = full_data.get(user_id, {})

os.makedirs("uploads", exist_ok=True)

def save_uploaded_image(uploaded_file):
    file_path = "uploads/" + user_id + "_" + uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def save_chats():
    try:
        with open("chats.json", "r") as f:
            full_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        full_data = {}

    full_data[user_id] = st.session_state.all_chats

    with open("chats.json", "w") as f:
        json.dump(full_data, f, indent=4)
st.markdown("""<style>:root {
    --bg-app:            #050a10;
    --bg-panel:          #0d1520;

    --sidebar-grad-1:    #061a30;
    --sidebar-grad-2:    #082b4b;
    --sidebar-grad-3:    #06182b;
    --sidebar-border:    #078cff;

    --accent:            #087eff;
    --accent-hover:      #149dff;
    --accent-soft:       rgba(8, 126, 255, 0.22);

    --danger:            #ff596a;
    --danger-bg:         #4a1822;
    --danger-soft:       rgba(255, 80, 100, 0.25);

    --bubble-user-bg:      #0b2233;
    --bubble-user-border:  rgba(8, 126, 255, 0.45);
    --bubble-assistant-bg: #10161d;
    --bubble-assistant-border: #263845;

    --avatar-user-bg:      var(--accent);
    --avatar-assistant-bg: #123b5b;
    --avatar-assistant-fg: #40cfff;

    --text-primary:      #f5f7fa;
    --text-secondary:    #dce7ee;
    --border-soft:       #24333e;
}

/* ---------- base app ---------- */
html, body, [data-testid="stAppViewContainer"],
.stApp, [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background: var(--bg-app) !important;
    color: var(--text-primary) !important;
}

/* Header: background only made transparent. Height is NOT forced to 0
   anymore — on newer Streamlit versions the sidebar collapse/expand
   button lives inside this header, and zeroing its height crushed
   that button, making it disappear entirely. */
header[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stMainMenu"] {
    display: none !important;
}

.block-container {
    width: 100% !important;
    max-width: 1450px !important;
    padding: 1rem 2rem 8rem 2rem !important;
}

/* ---------- sidebar shell ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        var(--sidebar-grad-1) 0%,
        var(--sidebar-grad-2) 48%,
        var(--sidebar-grad-3) 100%
    ) !important;
    border-right: 1px solid var(--sidebar-border) !important;
    box-shadow: 5px 0 30px rgba(0, 140, 255, 0.22) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1rem 0.8rem !important;
}

/* ---------- sidebar buttons (History / New Chat / chat list) ---------- */
section[data-testid="stSidebar"] button:not([data-testid*="Collapse"]):not([title*="idebar"]):not([aria-label*="idebar"]) {
    width: 100% !important;
    min-height: 48px !important;
    background: #0b3153 !important;
    color: var(--text-primary) !important;
    border: 1px solid #168fff !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(0, 117, 255, 0.22) !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] button:not([data-testid*="Collapse"]):not([title*="idebar"]):not([aria-label*="idebar"]):hover {
    background: #0d4775 !important;
    border-color: #35b8ff !important;
    box-shadow: 0 0 15px rgba(20, 160, 255, 0.42),
                0 5px 20px rgba(0, 100, 255, 0.25) !important;
}

section[data-testid="stSidebar"] button:not([data-testid*="Collapse"]):not([title*="idebar"]):not([aria-label*="idebar"]):active {
    transform: scale(0.97) !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
    gap: 7px !important;
    align-items: center !important;
    margin-bottom: 7px !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button {
    min-height: 42px !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:first-child {
    min-width: 0 !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:first-child button {
    text-align: left !important;
    padding-left: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:nth-child(2) {
    min-width: 42px !important;
    max-width: 42px !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:nth-child(2) button {
    width: 42px !important;
    min-width: 42px !important;
    padding: 0 !important;
    text-align: center !important;
    color: #d8efff !important;
}

section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div:nth-child(2) button:hover {
    color: var(--danger) !important;
    background: var(--danger-bg) !important;
    border-color: var(--danger) !important;
    box-shadow: 0 0 14px var(--danger-soft) !important;
}

section[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(55, 164, 235, 0.3) !important;
    margin: 16px 0 !important;
}

/* Case 1: collapse button while sidebar is open */
section[data-testid="stSidebar"] [data-testid*="Collapse"],
section[data-testid="stSidebar"] button[title*="idebar"] {
    background: #0b3153 !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    opacity: 1 !important;
    visibility: visible !important;
}

section[data-testid="stSidebar"] [data-testid*="Collapse"]:hover,
section[data-testid="stSidebar"] button[title*="idebar"]:hover {
    background: var(--accent) !important;
    box-shadow: 0 0 12px var(--accent-soft) !important;
}

section[data-testid="stSidebar"] [data-testid*="Collapse"] svg,
section[data-testid="stSidebar"] button[title*="idebar"] svg {
    fill: var(--text-primary) !important;
    color: var(--text-primary) !important;
}

/* Case 2: expand control floating in main area when collapsed */
[data-testid="stSidebarCollapsedControl"],
div[data-testid="collapsedControl"] {
    background: #0b3153 !important;
    border: 1px solid var(--accent) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45) !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebarCollapsedControl"] button,
div[data-testid="collapsedControl"] button,
button[title="Open sidebar"] {
    background: transparent !important;
    color: var(--text-primary) !important;
    border: none !important;
}

[data-testid="stSidebarCollapsedControl"]:hover,
div[data-testid="collapsedControl"]:hover {
    background: var(--accent) !important;
    box-shadow: 0 0 14px var(--accent-soft) !important;
}

[data-testid="stSidebarCollapsedControl"] svg,
div[data-testid="collapsedControl"] svg,
button[title="Open sidebar"] svg {
    fill: var(--text-primary) !important;
    color: var(--text-primary) !important;
}

/* ---------- chat bubbles ---------- */
div[data-testid="stChatMessage"] {
    width: 100% !important;
    max-width: 1050px !important;
    margin: 0.7rem auto !important;
    padding: 0.9rem 1.1rem !important;
    border-radius: 17px !important;
    background: var(--bubble-assistant-bg) !important;
    border: 1px solid var(--bubble-assistant-border) !important;
    box-shadow: 0 5px 22px rgba(0, 0, 0, 0.22) !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: var(--bubble-user-bg) !important;
    border-color: var(--bubble-user-border) !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: var(--bubble-assistant-bg) !important;
    border-color: var(--bubble-assistant-border) !important;
}

div[data-testid="stChatMessage"] p {
    color: var(--text-primary) !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}

div[data-testid="stChatMessage"] img {
    border-radius: 11px !important;
    border: 1px solid #38505f !important;
    object-fit: cover !important;
}

/* avatars — same accent family, no random unrelated hues */
div[data-testid="stChatMessageAvatarUser"] {
    background: var(--avatar-user-bg) !important;
    color: #ffffff !important;
}

div[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--avatar-assistant-bg) !important;
    color: var(--avatar-assistant-fg) !important;
}

/* ---------- chat input ---------- */
div[data-testid="stChatInput"] {
    width: 100% !important;
    max-width: 1050px !important;
    margin: 0 auto !important;
}

div[data-testid="stChatInput"] > div {
    background: #ffffff !important;
    border: 2px solid #cbd4dc !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.42) !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft),
                0 10px 35px rgba(0, 0, 0, 0.42) !important;
}

div[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #000000 !important;
    caret-color: #000000 !important;
    font-size: 15px !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #555555 !important;
    opacity: 1 !important;
}

div[data-testid="stChatInput"] button {
    background: var(--accent) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 11px !important;
}

div[data-testid="stChatInput"] button:hover {
    background: var(--accent-hover) !important;
    box-shadow: 0 0 15px var(--accent-soft) !important;
}

/* ---------- file uploader ---------- */
div[data-testid="stFileUploader"] {
    background: #101b25 !important;
    border: 1px dashed #2776a8 !important;
    border-radius: 14px !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-hover) !important;
    background: #112536 !important;
}

/* ---------- misc ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

hr {
    border: none !important;
    border-top: 1px solid var(--border-soft) !important;
    margin: 1rem 0 !important;
}

h1, h2, h3 {
    color: var(--text-primary) !important;
}

p, span, label {
    color: var(--text-secondary) !important;
}

::-webkit-scrollbar {
    width: 7px !important;
}

::-webkit-scrollbar-track {
    background: var(--bg-app) !important;
}

::-webkit-scrollbar-thumb {
    background: #214b6c !important;
    border-radius: 10px !important;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent) !important;
}

/* ---------- responsive ---------- */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    div[data-testid="stChatMessage"] {
        max-width: 100% !important;
        border-radius: 14px !important;
    }

    div[data-testid="stChatInput"] {
        max-width: 100% !important;
    }
}</style>
""", unsafe_allow_html=True)

if "all_chats" not in st.session_state:
    st.session_state.all_chats = all_chats

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = len(st.session_state.all_chats)

with st.sidebar:

    if st.button("HIstory 📜"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        st.write("Chat History")

        for chat_id in list(st.session_state.all_chats.keys()):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(chat_id, key=f"chat_{chat_id}"):
                    st.session_state.current_chat_id = chat_id
                    st.rerun()
            with col2:
                if st.button("🗑️",key=f"delete_{chat_id}"):
                    del st.session_state.all_chats[chat_id]

                    old_chats = list(st.session_state.all_chats.values())
                    st.session_state.all_chats = {}
                    for i, chat_data in enumerate(old_chats, start=1):
                        new_id = f"chat_{i}"
                        st.session_state.all_chats[new_id] = chat_data
                    st.session_state.chat_counter = len(st.session_state.all_chats)

                    if st.session_state.current_chat_id == chat_id:
                        if st.session_state.all_chats:
                            st.session_state.current_chat_id = list(
                                st.session_state.all_chats.keys()
                            )[0]
                        else:
                            st.session_state.current_chat_id = "chat_1"
                    save_chats()
                    st.rerun()

    if st.button("➕ New Chat"):
        st.session_state.chat_counter += 1
        new_chat_id = f"chat_{st.session_state.chat_counter}"

        st.session_state.all_chats[new_chat_id] = {
            "history": []
        }
        st.session_state.current_chat_id = new_chat_id
        st.rerun()

if st.session_state.current_chat_id is None:
    if st.session_state.all_chats:
        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]
    else:
        st.session_state.current_chat_id = "chat_1"

if st.session_state.current_chat_id not in st.session_state.all_chats:
    st.session_state.all_chats[st.session_state.current_chat_id] = {
        "history": []
    }

prompt = st.chat_input("Type your message...", accept_file="multiple")

if prompt:
    current_history = st.session_state.all_chats[st.session_state.current_chat_id]["history"]
    already_has_image = any(h.get("user_files") for h in current_history)

    if not already_has_image and not prompt.files:
        st.error("Please add atleast 1 image .......")
    else:
        with st.spinner("Plese wait for a while....."):
            time.sleep(1)
            dummy_reply = "Thats the backend answer"

        saved_image_paths = []

        for image in prompt.files:
            image_path = save_uploaded_image(image)
            saved_image_paths.append(image_path)


        # Backend work section ................................................................................

        st.session_state.all_chats[st.session_state.current_chat_id]["history"].append({
    "user_text": prompt.text,
    "user_files": saved_image_paths,
    "ai_reply": dummy_reply
        })
        save_chats()
        
for history in st.session_state.all_chats[st.session_state.current_chat_id]["history"]:
    col_empty1, col1 = st.columns([7, 3])
    with col1:
        with st.chat_message("user"):
            if history["user_text"]:
                st.write(history["user_text"])
            for image in history["user_files"]:
                st.image(image, width=120)

    st.divider()

    col2, col_empty2 = st.columns([7, 3])
    with col2:
        with st.chat_message("assistant"):
            st.write(history["ai_reply"])

    st.divider()
