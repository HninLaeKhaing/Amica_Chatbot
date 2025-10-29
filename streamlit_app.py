import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Amica AI", page_icon="💬", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* --- General Layout & Background --- */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff; /* Solid White */
    background-image: none;
}
[data-testid="stHeader"] {
    display: none; /* Hide default Streamlit header */
}

/* --- Header Section --- */
.amica-header {
    text-align: center;
    padding-top: 20px;
}
.amica-title {
    font-size: 2.5rem; /* Larger title */
    color: #000000;
    margin-bottom: 5px;
}
.amica-subtitle {
    font-size: 1.1rem;
    color: #666666;
    margin-bottom: 30px;
}
.amica-disclaimer-box {
    background-color: #f0f0f0; /* Light grey box for the disclaimer */
    border-radius: 10px;
    padding: 10px 15px;
    margin: 20px auto;
    width: 90%;
    max-width: 700px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border-left: 5px solid #ff4b4b; /* Red accent line */
    color: #333333;
    font-size: 0.9rem;
}

/* --- Chat Messages --- */
.stChatMessage {
    border-radius: 20px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Lighter shadow for cleaner look */
    border: none;
}

/* User Message (Blue Bubble, right-aligned) */
.stChatMessage[data-testid="stChatMessage"] > div:first-child[data-testid="stChatUserMessage"] {
    background-color: #2563eb; /* Blue */
    color: #ffffff;
    align-self: flex-end;
    border-bottom-right-radius: 5px; /* Sharp corner for the tail */
}

/* Bot Message (Light Blue/Pink Bubble, left-aligned) */
.stChatMessage[data-testid="stChatMessage"] > div:first-child[data-testid="stChatBotMessage"] {
    background-color: #e0f7fa; /* Very Light Cyan/Blue, similar to the image's light blue */
    color: #000000; /* Black text for readability */
    align-self: flex-start;
    border-bottom-left-radius: 5px; /* Sharp corner for the tail */
}

/* Override Streamlit's internal message padding */
[data-testid="stChatMessageContent"] {
    background-color: transparent !important;
    color: inherit !important;
}

/* --- Bot Avatar 'A' --- */
.avatar-bot {
    width: 30px; /* Smaller avatar */
    height: 30px;
    border-radius: 50%;
    background-color: #991b1b; /* Dark Red/Maroon */
    display: inline-flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    font-size: 16px;
    margin-right: 10px; /* Space between avatar and text */
}
.stChatBotMessage {
    display: flex;
    align-items: flex-start;
}
.stChatBotMessage > div:first-child {
    display: flex;
    flex-direction: row;
    align-items: center;
}

/* --- Input Area Styling (to remove default background) --- */
.stTextInput > div > div > input {
    border-radius: 20px;
    border: 1px solid #ccc;
    padding: 10px 15px;
}

/* --- Voice Button Styling --- */
.voice-button {
    background-color: #3b82f6; /* Blue */
    color: white;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: background-color 0.2s;
}
.voice-button:hover {
    background-color: #2563eb;
}
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
# NOTE: Replace with your actual Gemini API Key in a secure way (e.g., st.secrets)
# For this example, I'll keep the placeholder for functionality.
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDbdGmOXYtyddLjWhi_eOMr7JVjRg-J9ds") 

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

# --- HEADER (Visualisation Match) ---
st.markdown('<div class="amica-header">', unsafe_allow_html=True)
st.markdown('<div class="amica-title">Amica 💬</div>', unsafe_allow_html=True)
st.markdown('<div class="amica-subtitle">Your Mental Health Assistant</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<div class="amica-disclaimer-box">
    <b>Disclaimer:</b> I am not a substitute for professional therapy. If you are in crisis, please contact a local helpline immediately.
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# --- MODEL INIT ---
model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=SYSTEM_PROMPT)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False # Voice toggle

# --- HELPER FUNCTIONS ---

# --- DISPLAY HISTORY ---
def show_chat_history():
    for msg in st.session_state.chat.history:
        is_user = msg.role == "user"
        
        # Use a container to mimic the two-column bubble design
        if is_user:
            with st.chat_message("You", avatar=""): # No avatar needed for user
                st.markdown(msg.parts[0].text)
        else:
            with st.chat_message("Amica", avatar=""): # No avatar needed here, we'll use custom HTML
                # Wrap the content to include the custom 'A' avatar
                st.markdown(f'<div class="stChatBotMessage"><div class="avatar-bot">A</div> {msg.parts[0].text}</div>', unsafe_allow_html=True)

# --- SPEECH TO TEXT ---
def listen_to_mic():
    recognizer = sr.Recognizer()
    st.session_state.voice_input = "" # Clear previous input
    try:
        with sr.Microphone() as source:
            st.toast("🎤 Listening... Speak now.", icon="🎙️")
            st.session_state.listening = True
            time.sleep(0.5) # Give time for the toast to appear
            audio = recognizer.listen(source, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
            st.toast(f"You said: {text}", icon="✅")
            st.session_state.voice_input = text
    except sr.UnknownValueError:
        st.toast("Sorry, I didn’t catch that. Please try again.", icon="⚠️")
        st.session_state.voice_input = ""
    except sr.RequestError:
        st.toast("Speech recognition service unavailable.", icon="❌")
        st.session_state.voice_input = ""
    except Exception as e:
        st.toast(f"An error occurred: {e}", icon="❌")
        st.session_state.voice_input = ""
    finally:
        st.session_state.listening = False

# --- TEXT TO SPEECH ---
def speak_text(text):
    try:
        # st.toast("🔊 Speaking...", icon="🗣️")
        tts = gTTS(text, lang='en')
        # Use a temporary file to save and play the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.write_to_fp(tmp)
            temp_path = tmp.name
        
        # Display the audio player in the chat for voice response visualization
        st.audio(temp_path, format="audio/mp3", autoplay=True)
        os.remove(temp_path)
    except Exception as e:
        st.error(f"Error generating voice: {e}")

# --- CHAT LOGIC ---

def handle_chat_input(user_input):
    if not user_input:
        return

    # 1. Display User Message
    with st.chat_message("You", avatar=""):
        st.markdown(user_input)

    # 2. Check for safety keywords
    suicide_keywords = ["kill myself", "want to die", "commit suicide", "end my life", "suicidal"]
    if any(k in user_input.lower() for k in suicide_keywords):
        safety_response = "I'm very sorry to hear you're feeling this way... Please seek immediate help by contacting this helpline: 9152987821. You are not alone."
        with st.chat_message("Amica", avatar=""):
            st.markdown(f'<div class="stChatBotMessage"><div class="avatar-bot">A</div> {safety_response}</div>', unsafe_allow_html=True)
            if st.session_state.voice_enabled:
                speak_text(safety_response)
        st.session_state.chat.history.append({'role': 'user', 'parts': [{'text': user_input}]})
        st.session_state.chat.history.append({'role': 'model', 'parts': [{'text': safety_response}]})
    
    # 3. Get model response
    else:
        with st.spinner("Amica is thinking..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                model_text = response.text
            except Exception as e:
                model_text = f"I'm experiencing a problem right now. Error: {e}"

        # 4. Display model response
        with st.chat_message("Amica", avatar=""):
            st.markdown(f'<div class="stChatBotMessage"><div class="avatar-bot">A</div> {model_text}</div>', unsafe_allow_html=True)
            
            # 5. Speak text if voice is enabled
            if st.session_state.voice_enabled:
                speak_text(model_text)

# --- DISPLAY HISTORY BEFORE INPUT ---
show_chat_history()

# --- INPUT AND VOICE TOGGLE SECTION ---
# Use an empty container for the input area to keep it at the bottom
input_container = st.container()

with input_container:
    # Use columns to align the text input and the voice button
    col1, col2 = st.columns([10, 1])

    # 1. Text Input (col1)
    with col1:
        # Ensure the chat_input returns the value to a variable, not a key
        user_prompt = st.chat_input("Type how you feel", key="text_input")

    # 2. Voice Button (col2)
    # The voice button is a standard Streamlit button that controls the voice_enabled state
    with col2:
        # Use a custom button style to look like the image's mic button
        if st.button("🔊", key="voice_toggle", help="Toggle Voice Response (Text-to-Speech)"):
            st.session_state.voice_enabled = not st.session_state.voice_enabled
            if st.session_state.voice_enabled:
                st.toast("Voice Response **Enabled**! Amica will speak her replies. 🔊", icon="✅")
            else:
                st.toast("Voice Response **Disabled**. 🔇", icon="🛑")
        
        # Add a visual indicator for the voice state
        if st.session_state.voice_enabled:
             st.markdown('<style>#voice_toggle { background-color: #ff4b4b; }</style>', unsafe_allow_html=True)
        else:
            st.markdown('<style>#voice_toggle { background-color: #3b82f6; }</style>', unsafe_allow_html=True)
        
        # The microphone button for Speech-to-Text (optional, but good for voice input)
        # if st.button("🎙️", key="mic_input", help="Click to speak your message"):
        #     listen_to_mic() # This triggers the microphone listening

# --- RUN CHAT FLOW ---

# Handle text input
if user_prompt:
    handle_chat_input(user_prompt)
    st.rerun() # Rerun to clear input and update history

# # Handle voice input (if you were to implement the mic button for input)
# if st.session_state.get("voice_input"):
#     handle_chat_input(st.session_state.voice_input)
#     st.session_state.voice_input = "" # Clear after use
#     st.rerun()
