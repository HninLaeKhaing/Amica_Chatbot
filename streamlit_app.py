import google.generativeai as genai

import speech_recognition as sr

from gtts import gTTS

import tempfile

import os



# --- PAGE CONFIG ---

st.set_page_config(page_title="Kura AI", page_icon="🧠", layout="centered")



# --- CUSTOM CSS ---

st.markdown("""

<style>

[data-testid="stAppViewContainer"] {

    background-image: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);

}

.stChatMessage {

    border-radius: 20px;

    padding: 1rem 1.5rem;

    margin-bottom: 1rem;

    box-shadow: 0 4px 10px rgba(0,0,0,0.2);

    border: 1px solid rgba(255,255,255,0.1);

}

[data-testid="stChatMessageContent"] {

    background-color: #ffffff;

    color: #1f2937;

}

[data-testid="stChatMessageContent"]:has(.avatar-bot) {

    background-color: #2563eb;

    color: #ffffff;

}

.stChatMessage > div:first-child {

  display: flex;

  flex-direction: column;

  align-items: center;

}

[data-testid="stChatMessageContent"] .avatar-bot {

    width: 50px;

    height: 50px;

    border-radius: 50%;

    background-color: #991b1b;

    display: flex;

    justify-content: center;

    align-items: center;

    color: white;

    font-weight: bold;

    font-size: 24px;

    margin-bottom: 0.5rem;

}

h1 { color: #ffffff; text-align: center; }

[data-testid="stWarning"] {

    background-color: #1e293b;

    border-radius: 15px;

    border-color: #3b82f6;

    color: #e2e8f0;

}

</style>

""", unsafe_allow_html=True)



# --- API CONFIG ---

API_KEY = "AIzaSyAs-vkAA9MB405bzY3lSsMJtb0VsxScbSc"



try:

    genai.configure(api_key=API_KEY)

except Exception as e:

    st.error(f"API configuration error: {e}")

    st.stop()



# --- SYSTEM PROMPT ---

SYSTEM_PROMPT = """

You are Kura, a highly empathetic and caring AI assistant focused on mental well-being.

You are a supportive and non-judgmental listener.

Always acknowledge the user's feelings and respond warmly.

If a user expresses suicidal thoughts, say:

"I'm very sorry to hear you're feeling this way, but please seek immediate help by contacting this helpline: 9152987821. You are not alone."

Never diagnose or prescribe. Always stay comforting and safe.

"""



# --- HEADER ---

st.markdown('<div style="text-align: center;"><h1>Kura - Your Mental Health Assistant 💬</h1></div>', unsafe_allow_html=True)

st.warning("*Disclaimer:* I am not a substitute for professional therapy. If you are in crisis, please contact a local helpline immediately.")

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

                st.markdown('<div class="avatar-bot">K</div>', unsafe_allow_html=True)

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

    return ""
