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
/* Background for a calm, soothing feel */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(135deg, #e0f2f1 0%, #b2ebf2 100%); /* Light Teal/Aqua Gradient */
}

/* Base chat message container style */
.stChatMessage {
    border-radius: 20px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1); /* Softer shadow */
    border: 1px solid rgba(0,0,0,0.05); /* Very light border */
}

/* User chat message content (Soft Green) */
[data-testid="stChatMessageContent"]:has(div:not(.avatar-bot)) {
    background-color: #f1f8e9; /* Very light green, almost white */
    color: #38761d; /* Dark green text for readability */
}

/* Bot chat message content (Calm Blue) */
[data-testid="stChatMessageContent"]:has(.avatar-bot) {
    background-color: #e3f2fd; /* Very light blue */
    color: #1565c0; /* Medium blue text */
}

/* Aligning avatar/name for all messages */
.stChatMessage > div:first-child {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Aligned to the left for better reading flow */
}

/* Bot avatar style (Gentle Purple/Lavender) */
[data-testid="stChatMessageContent"] .avatar-bot {
    width: 40px; /* Slightly smaller avatar */
    height: 40px;
    border-radius: 50%;
    background-color: #90a4ae; /* Muted grey-blue for neutrality/calm */
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 0.5rem;
    margin-right: 0.5rem; /* Space between avatar and text if needed */
}

/* Header text color */
h1 { 
    color: #00796b; /* Dark Teal for a professional and calm heading */
    text-align: center; 
}

/* Warning box style (for disclaimer) */
[data-testid="stWarning"] {
    background-color: #fffde7; /* Very light yellow for gentle notice */
    border-radius: 15px;
    border-color: #ffb300; /* Amber border */
    color: #5d4037; /* Dark text for contrast */
}

/* Input box styling for consistency */
[data-testid="stChatInput"] {
    border-top: 1px solid #b2ebf2;
    padding-top: 10px;
    background-color: #ffffff; /* White input background */
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
