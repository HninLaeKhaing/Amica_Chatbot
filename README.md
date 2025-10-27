# 🧠 Amica AI: Your Empathetic Mental Health Assistant 💬

Amica AI is a **Streamlit-based chatbot** powered by the **Google Gemini-2.5-Pro model**, designed to offer **supportive and non-judgmental listening** for mental well-being. It integrates both **text-based chat** and **voice interaction** (Speech-to-Text and Text-to-Speech) to provide an engaging and accessible user experience.

---

## ✨ Features

* **Empathetic AI Persona:** The Gemini-2.5-Pro model is configured with a specific system prompt to act as "Amica," a highly empathetic, non-judgmental, and caring mental health companion.
* **Critical Safety Override:** Implements a strict, hardcoded safety check for suicide-related keywords. If triggered, it immediately provides a pre-defined safety message and the helpline number **`911`**, overriding the standard AI response.
* **Voice Input (STT):** Uses the `speech_recognition` library to transcribe user speech from a microphone into text input.
* **Voice Output (TTS):** Uses the `gTTS` library to convert Amica's text responses into speech, played back directly in the Streamlit interface.
* **Custom UI/UX:** Features a highly customized Streamlit interface with a clean, white background and distinct, visually appealing chat bubble styling.
* **Session History:** Maintains the conversation history across interactions within a single session.

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8+
* A **Google AI API Key** for the Gemini model.



### ⚠️ Important Disclaimer
    
Amica AI is not a substitute for professional therapy, psychological, or medical advice. It is an AI tool designed for supportive listening and informational purposes only. If you are experiencing a mental health crisis or suicidal thoughts, please contact a local emergency service or a professional helpline immediately.
