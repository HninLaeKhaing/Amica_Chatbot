# 🧠 Amica AI: Your Empathetic Mental Health Assistant 💬

Amica AI is a **Streamlit-based chatbot** powered by the **Google Gemini-2.5-Pro model**, designed to offer **supportive and non-judgmental listening** for mental well-being. It integrates both **text-based chat** and **voice interaction** (Speech-to-Text and Text-to-Speech) to provide an engaging and accessible user experience.

---

## ✨ Features

* **Empathetic AI Persona:** The Gemini-2.5-Pro model is configured with a specific system prompt to act as "Amica," a highly empathetic, non-judgmental, and caring mental health companion.
* **Critical Safety Override:** Implements a strict, hardcoded safety check for suicide-related keywords. If triggered, it immediately provides a pre-defined safety message and the helpline number **`9152987821`**, overriding the standard AI response.
* **Voice Input (STT):** Uses the `speech_recognition` library to transcribe user speech from a microphone into text input.
* **Voice Output (TTS):** Uses the `gTTS` library to convert Amica's text responses into speech, played back directly in the Streamlit interface.
* **Custom UI/UX:** Features a highly customized Streamlit interface with a clean, white background and distinct, visually appealing chat bubble styling.
* **Session History:** Maintains the conversation history across interactions within a single session.

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8+
* A **Google AI API Key** for the Gemini model.

### 1. Save the Code

Save the provided Python script into a file named **`app.py`**.

### 2. Install Dependencies

Install all necessary Python packages using pip:

```bash
pip install streamlit google-genai speechrecognition gtts
# Note: On some systems, especially for microphone use, you might also need to install PyAudio.

3. Configure API Key (Crucial Step)

For security, use an environment variable instead of hardcoding the key.

    Set the environment variable (replace YOUR_ACTUAL_API_KEY):
    Bash

    export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"

    Modify app.py to read the key securely. You should change the API configuration block in your script to use os.environ.get() instead of a literal string.

🏃 How to Run the Application

    Ensure your dependencies are installed and the GEMINI_API_KEY environment variable is set in your terminal session.

    Run the Streamlit application:
    Bash

    streamlit run app.py

    The application will automatically open in your default web browser (usually at http://localhost:8501).

⚠️ Important Disclaimer

    Amica AI is not a substitute for professional therapy, psychological, or medical advice. It is an AI tool designed for supportive listening and informational purposes only. If you are experiencing a mental health crisis or suicidal thoughts, please contact a local emergency service or a professional helpline immediately.
