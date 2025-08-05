!pip install -r requirements.txt

import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
import streamlit as st
from chatbot import chatbot_response

st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")

st.title("🧠 Mental Health Chatbot")
st.write("Hello! I'm here to listen. How are you feeling today?")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Tell me how you feel...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
