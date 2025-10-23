import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Amica AI", page_icon="🧠", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* Background: Deep Slate/Charcoal Gradient for elegance and focus */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(135deg, #1b263b 0%, #0d121c 100%); /* Deep Navy/Slate Gradient */
}

/* Base chat message container style */
.stChatMessage {
    border-radius: 15px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4); /* Deeper shadow for elevation */
    border: 1px solid rgba(255,255,255,0.1); /* Subtle white border */
}

/* User chat message content (Soft White/Cream on Dark) */
/* Note: Since the background is dark, the user content should be light for contrast */
[data-testid="stChatMessageContent"]:has(div:not(.avatar-bot)) {
    background-color: #384250; /* Muted dark blue-gray */
    color: #f0f4f8; /* Soft white text */
}

/* Bot chat message content (A gentle contrast color, like Muted Blue-Green) */
[data-testid="stChatMessageContent"]:has(.avatar-bot) {
    background-color: #4a5c6a; /* Slate Blue-Gray */
    color: #c4d4e3; /* Very light blue-gray text */
}

/* Aligning avatar/name for all messages */
.stChatMessage > div:first-child {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* Bot avatar style (Classic Gold/Brass for an elegant touch) */
[data-testid="stChatMessageContent"] .avatar-bot {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #8a6c4c; /* Muted Gold/Brass */
    display: flex;
    justify-content: center;
    align-items: center;
    color: #f0f4f8; /* Soft white text */
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 0.5rem;
    margin-right: 0.5rem;
}

/* Header text color (Subtle Gold/Cream on Dark) */
h1 { 
    color: #c4d4e3; /* Light Gray-Blue */
    text-align: center; 
}

/* Warning box style (for disclaimer - maintaining elegance with dark contrast) */
[data-testid="stWarning"] {
    background-color: #2b3a4a; /* Darker background */
    border-radius: 15px;
    border-color: #8a6c4c; /* Gold/Brass border */
    color: #f0f4f8; /* Soft white text */
}

/* Info box style (for listening notification) */
[data-testid="stInfo"] {
    background-color: #384250;
    color: #f0f4f8;
    border-color: #4a5c6a;
}

/* Input box styling for consistency */
[data-testid="stChatInput"] {
    border-top: 1px solid #384250;
    padding-top: 10px;
    background-color: #1b263b; /* Dark input background matching main background */
}
/* Ensure the input text is visible */
[data-testid="stChatInput"] input {
    color: #f0f4f8;
}
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
API_KEY = "AIzaSyDbdGmOXYtyddLjWhi_eOMr7JVhRg-J9ds"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API configuration error: {e}")
    st.stop()

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are Amica, a highly empathetic and caring AI assistant focused on mental well-being.
You are a supportive and non-judgmental listener.
Always acknowledge the user's feelings and respond warmly.
If a user expresses suicidal thoughts, say:
"I'm very sorry to hear you're feeling this way, but please seek immediate help by contacting this helpline: 9152987821. You are not alone."
Never diagnose or prescribe. Always stay comforting and safe.
"""

# --- HEADER ---
st.markdown('<div style="text-align: center;"><h1>Amica - Your Mental Health Assistant 💬</h1></div>', unsafe_allow_html=True)
st.warning("**Disclaimer:** I am not a substitute for professional therapy. If you are in crisis, please contact a local helpline immediately.")
st.markdown("---")

# --- MODEL INIT ---
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM_PROMPT)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- DISPLAY HISTORY ---
def show_chat_history():
    for msg in st.session_state.chat.history:
        is_user = msg.role == "user"
        with st.chat_message("You" if is_user else "Kura"):
            if not is_user:
                st.markdown('<div class="avatar-bot">A</div>', unsafe_allow_html=True)
            st.markdown(msg.parts[0].text)
show_chat_history()

# --- SPEECH TO TEXT ---
def listen_to_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        audio = recognizer.listen(source, phrase_time_limit=6)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I didn’t catch that. Please try again.")
        except sr.RequestError:
            st.error("Speech recognition service unavailable.")
    return ""

# --- TEXT TO SPEECH ---
def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name, format="audio/mp3")
        os.remove(tmp.name)

# --- CHAT LOGIC ---
col1, col2 = st.columns([1, 1])
with col1:
    user_prompt = st.chat_input("Type how you feel")

if user_prompt:
    with st.chat_message("You"):
        st.markdown(user_prompt)

    suicide_keywords = ["kill myself", "want to die", "commit suicide", "end my life", "suicidal"]
    if any(k in user_prompt.lower() for k in suicide_keywords):
        safety_response = "I'm very sorry to hear you're feeling this way... Please seek help immediately by contacting this helpline: 9152987821."
        with st.chat_message("Amica"):
            st.markdown('<div class="avatar-bot">A</div>', unsafe_allow_html=True)
            st.markdown(safety_response)
            speak_text(safety_response)
        st.session_state.chat.history.append({'role': 'user', 'parts': [{'text': user_prompt}]})
        st.session_state.chat.history.append({'role': 'model', 'parts': [{'text': safety_response}]})
    else:
        response = st.session_state.chat.send_message(user_prompt)
        with st.chat_message("Amica"):
            st.markdown('<div class="avatar-bot">A</div>', unsafe_allow_html=True)
            st.markdown(response.text)
            speak_text(response.text)
