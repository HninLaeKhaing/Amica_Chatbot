import streamlit as st
import tempfile
import base64
import google.generativeai as genai

# -----------------------------
# CONFIGURE GEMINI API
# -----------------------------
st.set_page_config(page_title="AI Mental Health Voice Chatbot", page_icon="💬", layout="centered")

st.title("🧠 AI Mental Health Chatbot (Voice + Text)")
st.markdown("### Speak or type to share how you feel 💬")

# -----------------------------
# Gemini API Key Setup
# -----------------------------
api_key = st.secrets.get("AIzaSyAs-vkAA9MB405bzY3lSsMJtb0VsxScbSc", None)
if not api_key:
    st.error("Please add your Gemini API key in Streamlit Secrets (Settings → Secrets).")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# -----------------------------
# FUNCTION: Process Audio (Browser Input)
# -----------------------------
def get_voice_input():
    st.subheader("🎙️ Speak your thoughts")
    audio_input = st.audio_input("Record your message")

    if audio_input:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_input.read())
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()

        # Send audio to Gemini for transcription
        st.info("🔍 Processing your voice...")
        response = model.generate_content([
            {"role": "user", "parts": [
                {"mime_type": "audio/wav", "data": base64.b64encode(audio_bytes).decode()},
                {"text": "Transcribe this voice message and summarize the emotion behind it."}
            ]}
        ])
        return response.text

    return None

# -----------------------------
# FUNCTION: Get Gemini Chatbot Reply
# -----------------------------
def get_chatbot_reply(prompt):
    full_prompt = (
        "You are a kind, empathetic mental health assistant. "
        "Always reply with supportive, calm, and encouraging language.\n\n"
        f"User: {prompt}\nTherapist:"
    )
    response = model.generate_content(full_prompt)
    return response.text

# -----------------------------
# MAIN APP
# -----------------------------
tab1, tab2 = st.tabs(["🎤 Voice Mode", "⌨️ Text Mode"])

with tab1:
    user_message = get_voice_input()
    if user_message:
        st.write(f"🗣️ You said: **{user_message}**")
        bot_reply = get_chatbot_reply(user_message)
        st.success(f"🤖 Chatbot: {bot_reply}")

with tab2:
    user_text = st.text_input("How are you feeling today?")
    if st.button("Send"):
        if user_text:
            bot_reply = get_chatbot_reply(user_text)
            st.success(f"🤖 Chatbot: {bot_reply}")
        else:
            st.warning("Please type something first!")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini AI")
