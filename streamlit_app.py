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
/* CHANGED: Background color to white */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff; /* Solid White */
    background-image: none; /* Removed gradient to ensure solid white */
}
.stChatMessage {
    border-radius: 20px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    /* CHANGED: Adjusted border for visibility on white background */
    border: 1px solid rgba(0,0,0,0.1); 
}
[data-testid="stChatMessageContent"] {
    background-color: light pink;
    color: indigo;
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
/* CHANGED: Header color to black for readability on white background */
h1 { color: #000000; text-align: center; } 
[data-testid="stWarning"] {
    background-color: #1e293b;
    border-radius: 15px;
    border-color: #3b82f6;
    /* CHANGED: Warning text color to dark grey for readability on white page background */
    color: #333333; 
}
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
API_KEY = "AIzaSyDbdGmOXYtyddLjWhi_eOMr7JVjRg-J9ds"

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
        with st.chat_message("You" if is_user else "Amica"):
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
            st.markdown('<di<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amica: The Clinically-Informed Mental Wellness Companion</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Use Inter font family -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #87CEEB; /* Very light background */
        }
        .section-card {
            border-radius: 1.5rem;
            box-shadow: 0 8px 16px rgba(17, 24, 39, 0.05);
        }
        .chat-container {
            height: 400px; /* Fixed height for chat window */
            overflow-y: auto;
            background-color: #ffffff;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb;
        }
        .user-message {
            background-color: #a5b4fc; /* Light Indigo */
            color: #1e3a8a; /* Dark Blue */
            max-width: 80%;
        }
        .amica-message {
            background-color: #fce7f3; /* Light Pink */
            color: #831843; /* Dark Pink */
            max-width: 80%;
        }
        /* Style for the subtle sign-in/session indicator */
        .session-indicator {
            background-color: #eff6ff; /* Blue background for session info */
            color: #3b82f6; /* Blue text */
        }
        .demo-mode-indicator {
            background-color: #fef3c7; /* Yellow background for demo warning */
            color: #d97706; /* Dark yellow/orange text */
        }
    </style>

    <style>
a:link {
  color: green;
  background-color: transparent;
  text-decoration: none;
}

a:visited {
  color: indigo;
  background-color: transparent;
  text-decoration: none;
}

a:hover {
  color: red;
  background-color: transparent;
  text-decoration: underline;
}

a:active {
  color: yellow;
  background-color: transparent;
  text-decoration: underline;
}
</style>
    <!-- Firebase SDK imports and authentication logic -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";
        import { setLogLevel } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";
        setLogLevel('Debug');

        // --- GLOBAL STATE & FIREBASE INITIALIZATION ---
        window.USER_STATE = {
            chat_history: [] // Stores conversation for Gemini API context
        };
        window.isAuthenticated = false; // Initial authentication status
        window.isDemoMode = false; // Flag for API bypass
        
        // Mandatory global variables provided by the environment
        const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
        const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
        
        let db, auth;
        const isFirebaseConfigured = Object.keys(firebaseConfig).length > 0;

        // Function to toggle UI visibility based on auth state
        const toggleChatVisibility = (isAuth) => {
            const chatSection = document.getElementById('chatbot-section');
            const authButtonsDiv = document.getElementById('auth-buttons');
            const sessionIdElement = document.getElementById('user-session-id');
            const modeIndicator = document.getElementById('mode-indicator');

            // Toggles the visibility of the main personalized section
            if (chatSection) {
                 // The chat section is visible if authenticated OR if running in demo mode
                const shouldShowChat = isAuth || !isFirebaseConfigured;
                chatSection.classList.toggle('hidden', !shouldShowChat);
                window.isAuthenticated = shouldShowChat; // Update global state for chat gatekeeping
            }
            
            // Update auth buttons and session indicator
            authButtonsDiv.innerHTML = ''; // Clear existing buttons

            if (isAuth && isFirebaseConfigured) {
                // AUTHENTICATED MODE
                const userId = auth.currentUser.uid;
                sessionIdElement.textContent = `User ID: ${userId}`;
                sessionIdElement.title = `Full User ID: ${userId}`;
                modeIndicator.textContent = 'Mode: Live';
                modeIndicator.className = 'px-3 py-1 text-xs font-semibold rounded-full session-indicator transition duration-150';
                
                // Sign Out Button
                const signOutButton = document.createElement('button');
                signOutButton.className = 'px-4 py-2 text-sm font-semibold rounded-lg text-red-600 border border-red-600 hover:bg-red-50 transition duration-150';
                signOutButton.textContent = 'Sign Out';
                signOutButton.onclick = async () => {
                    await signOut(auth);
                    window.USER_STATE.chat_history = []; // Clear history on sign out
                };
                authButtonsDiv.appendChild(signOutButton);

            } else if (!isAuth && isFirebaseConfigured) {
                // LOGGED OUT MODE (Firebase configured)
                sessionIdElement.textContent = 'Session: Anonymous';
                sessionIdElement.title = 'You are browsing anonymously.';
                modeIndicator.textContent = 'Mode: Offline';
                modeIndicator.className = 'px-3 py-1 text-xs font-semibold rounded-full bg-gray-200 text-gray-500 transition duration-150';

                // Sign In Button (simulates login)
                const signInButton = document.createElement('button');
                signInButton.className = 'px-4 py-2 text-sm font-semibold rounded-lg text-indigo-600 border border-indigo-600 hover:bg-indigo-50 transition duration-150';
                signInButton.textContent = 'Sign In';
                signInButton.onclick = authenticate; 
                authButtonsDiv.appendChild(signInButton);

                // Sign Up Button (simulates sign up)
                const signUpButton = document.createElement('button');
                signUpButton.className = 'px-4 py-2 text-sm font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition duration-150 shadow-md';
                signUpButton.textContent = 'Sign Up';
                signUpButton.onclick = authenticate; 
                authButtonsDiv.appendChild(signUpButton);

            } else {
                // DEMO MODE (Firebase NOT configured)
                sessionIdElement.textContent = 'Session: Demo';
                sessionIdElement.title = 'Firebase is not configured. Chat is active but data is not persistent.';
                modeIndicator.textContent = 'Mode: Demo (API Disabled)';
                modeIndicator.className = 'px-3 py-1 text-xs font-semibold rounded-full demo-mode-indicator transition duration-150';
            }
        };

        async function authenticate() {
            if (!isFirebaseConfigured) {
                console.warn("Firebase config not found. Cannot authenticate.");
                return;
            }
            try {
                if (initialAuthToken) {
                    await signInWithCustomToken(auth, initialAuthToken);
                    console.log("Firebase signed in with custom token.");
                } else {
                    await signInAnonymously(auth);
                    console.log("Firebase signed in anonymously.");
                }
            } catch (error) {
                console.error("Firebase authentication error:", error);
            }
        }
        
        if (isFirebaseConfigured) {
            window.firebaseApp = initializeApp(firebaseConfig);
            db = getFirestore(window.firebaseApp);
            auth = getAuth(window.firebaseApp);
            
            // Listener to handle authentication state changes
            onAuthStateChanged(auth, (user) => {
                const isAuth = !!user;
                toggleChatVisibility(isAuth);
                if (user) {
                    window.currentUserId = user.uid;
                }
            });
            authenticate(); // Initial attempt to sign in on load
        } else {
            console.warn("Firebase configuration not found. Running in DEMO MODE.");
            window.isDemoMode = true;
            // Directly call toggle with false auth state to trigger Demo Mode UI logic
            toggleChatVisibility(false); 
        }

        // --- DEMO MODE RESPONSES ---
        const demoResponses = [
            "I hear the feeling of overwhelm. It sounds heavy. Could you tell me one specific thing that is making you feel this way right now?",
            "That's a valid feeling. Let's take a deep breath together. When we break down big feelings into smaller pieces, they often feel more manageable. What small step can you take today?",
            "It sounds like you are carrying a lot. Remember, your feelings are signals, not facts. What is one supportive thought you could offer yourself right now?",
            "Thank you for sharing that with me. That takes courage. Let's explore that thought a little deeper using the CBT framework. What evidence supports that thought, and what evidence challenges it?",
            "I'm here for you. We can try a quick grounding exercise if that would help. Can you name three things you can see, two things you can hear, and one thing you can touch?"
        ];

        let demoResponseIndex = 0;

        const getDemoResponse = () => {
            const response = demoResponses[demoResponseIndex];
            demoResponseIndex = (demoResponseIndex + 1) % demoResponses.length; // Cycle through responses
            return { response: response, success: true, actionCommand: "DEMO_MODE: Bypassed_API" };
        };


        // --- GEMINI API INTEGRATION (Now includes Demo Mode Fallback) ---
        
        /**
         * Calls the Gemini API to get Amica's response, or uses demo mode if unavailable.
         */
        window.callGeminiApi = async (prompt) => {
            if (window.isDemoMode) {
                return getDemoResponse();
            }

            const apiKey = ""; 
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

            // System prompt defining Amica's persona
            const systemPrompt = "You are Amica, a compassionate and non-judgmental mental wellness robot designed on Cognitive Behavioral Therapy (CBT) principles. Your goal is to provide supportive, reflective, and clinically-informed responses. Keep your responses concise, empathetic, and focus on validating the user's feelings while subtly guiding them towards self-awareness and coping skills. DO NOT provide medical advice; always defer to professional help in crisis. Never mention API keys or technical terms.";
            
            // Map our internal chat history format to the API format (model/user roles)
            const chatHistory = window.USER_STATE.chat_history.map(msg => ({
                role: msg.role === 'amica' ? 'model' : 'user',
                parts: [{ text: msg.text }]
            }));
            
            // Add the current user prompt
            chatHistory.push({ role: 'user', parts: [{ text: prompt }] });

            const payload = {
                contents: chatHistory,
                systemInstruction: {
                    parts: [{ text: systemPrompt }]
                },
                tools: [{ "google_search": {} }], 
            };

            const options = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            };

            try {
                // Use fetch with retry for robust API calls
                const response = await fetchWithRetry(apiUrl, options);
                const result = await response.json();
                
                const text = result?.candidates?.[0]?.content?.parts?.[0]?.text;
                
                if (text) {
                    return { response: text, success: true, actionCommand: "API_Success: Generated_Response" };
                } else {
                    // If the API returns a valid response object but no text (e.g., filtered content)
                    const noTextError = "API response received, but no content generated (potential safety filter).";
                    console.error(noTextError, result);
                    throw new Error(noTextError);
                }
            } catch (error) {
                // If the real API call fails, switch to demo mode for this and future calls
                console.error("API call failed. Falling back to Demo Mode.", error);
                window.isDemoMode = true; // Permanent switch to demo mode for the session
                document.getElementById('mode-indicator').textContent = 'Mode: Demo (API FAILED)';
                document.getElementById('mode-indicator').className = 'px-3 py-1 text-xs font-semibold rounded-full demo-mode-indicator transition duration-150';

                // Return a specific demo response to acknowledge the error and provide a first response
                return { 
                    response: "I seem to be experiencing some technical difficulties connecting to my core intelligence. For now, I can provide supportive, pre-programmed guidance to help you focus on the present moment.", 
                    success: true, 
                    actionCommand: `FALLBACK_TO_DEMO: ${error.message || 'Unknown Network Error'}` 
                };
            }
        };
        
        // --- Remaining Helper Functions ---
        async function fetchWithRetry(url, options, maxRetries = 5, delay = 1000) {
            for (let i = 0; i < maxRetries; i++) {
                try {
                    const response = await fetch(url, options);
                    if (!response.ok) {
                        // Throw an error on non-2xx response codes
                        const errorBody = await response.text();
                        const errorMsg = `HTTP error! status: ${response.status}`;
                        console.error(errorMsg, errorBody);
                        throw new Error(errorMsg); // Throw the error for window.callGeminiApi to catch
                    }
                    return response;
                } catch (error) {
                    if (i === maxRetries - 1) {
                        console.error("Max retries reached. Failing request.", error);
                        throw error;
                    }
                    // Exponential backoff
                    await new Promise(res => setTimeout(res, delay));
                    delay *= 2; 
                }
            }
        }
    </script>
</head>
<body class="min-h-screen flex flex-col items-center">

    <!-- Navigation Bar -->
    <nav class="w-full bg-white shadow-sm sticky top-0 z-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <span class="text-2xl font-extrabold">
                        <span class="text-indigo-600">Amica</span>
                        <span class="text-pink-500">.ai</span>
                    </span>
                </div>
                <!-- Navigation Links -->
                <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <a href="#about" class="text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-indigo-600 transition">About Amica</a>
                    <a href="#knowledge" class="text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-indigo-600 transition">Knowledge</a>
                    <a href="#team" class="text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-indigo-600 transition">Our Team</a>
                    <a href="#chatbot-section" class="text-gray-900 inline-flex items-center px-1 pt-1 text-sm font-medium hover:text-indigo-600 transition">Start Chat</a>
                </div>
                <!-- Auth Buttons & Session Info -->
                <div class="flex items-center space-x-4">
                    <div id="mode-indicator" class="px-3 py-1 text-xs font-semibold rounded-full session-indicator transition duration-150">
                        Loading Mode...
                    </div>
                    <div id="user-session-id" class="text-xs font-mono px-3 py-1 rounded-full session-indicator transition duration-150">
                        Loading Session...
                    </div>
                    <!-- Auth Buttons are managed dynamically by JavaScript -->
                    <div id="auth-buttons" class="flex items-center space-x-3">
                        <!-- Initial placeholder buttons (will be replaced by JS) -->
                        <button class="px-4 py-2 text-sm font-semibold rounded-lg text-indigo-600 border border-indigo-600">Sign In</button>
                        <button class="px-4 py-2 text-sm font-semibold rounded-lg bg-indigo-600 text-white">Sign Up</button>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content Area -->
    <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-12 space-y-20">

        <!-- 1. Hero / About the Amica Robot -->
        <section id="about" class="section-card bg-white p-10 border border-gray-100 flex flex-col md:flex-row items-center gap-10">
            <div class="md:w-3/5 space-y-6">
                <h2 class="text-5xl font-extrabold text-gray-900 leading-tight">
                    The Future of Mental Wellness is <span class="text-indigo-600">Personal</span>.
                </h2>
                    
                <p class="text-xl text-gray-600">
                    Amica is not just an AI; it's a dedicated mental wellness chatbot + robot built on principles of **Cognitive Behavioral Therapy (CBT)** and **ethical safety**. Our core technology, the Core Intelligence Module (CIM), ensures every interaction is timely, empathetic, and tailored to your personal journey, providing supportive care right when you need it.
                    <a href="https://amicarobot-mwq6taxcz847ppunwsotpb.streamlit.app/"> Get Free Amica Chatbot Here!</a>
                </p>
                
                
                <ul class="space-y-2 text-gray-700">
                    <li class="flex items-center"><span class="text-green-500 mr-3 text-xl">&check;</span>Clinically-informed CBT techniques.</li>
                    <li class="flex items-center"><span class="text-green-500 mr-3 text-xl">&check;</span>24/7, non-judgmental, immediate support.</li>
                    <li class="flex items-center"><span class="text-green-500 mr-3 text-xl">&check;</span>Data-driven goal tracking and progress review.</li>
                </ul>
            </div>
            <div class="md:w-2/5 flex justify-center">
                <!-- AMICA ROBOT IMAGE: The image path is now a standard relative path, assuming 'robot.jpg' is in an 'assets' folder -->
                <div class="p-8 bg-pink-100 rounded-full shadow-xl overflow-hidden">
                    <img src="assets/robot.jpg" 
                         onerror="this.onerror=null; this.src='https://placehold.co/192x192/fce7f3/db2777?text=Amica+Robot'"
                         alt="Amica Robot Illustration" 
                         class="h-60 w-60 object-cover rounded-full">
                </div>
            </div>
        </section>

        <!-- 2. Mental Health Knowledge Sharing Section -->
        <section id="knowledge" class="space-y-10">
            <h2 class="text-4xl font-bold text-center text-gray-800">Knowledge-Driven Care</h2>
            <p class="text-center text-lg text-gray-600 max-w-3xl mx-auto">Amica's responses are grounded in accredited therapeutic practices, ensuring a safe and beneficial supportive experience.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="section-card p-6 bg-green-50 border border-green-200 hover:shadow-lg transition">
                    <h3 class="font-bold text-2xl text-green-700 mb-3">Structured Skill Building</h3>
                    <p class="text-base text-gray-600 leading-relaxed">Amica guides you through **identifying and challenging unhelpful thoughts** using proven Cognitive Behavioral Therapy frameworks.</p>
                </div>
                <div class="section-card p-6 bg-blue-50 border border-blue-200 hover:shadow-lg transition">
                    <h3 class="font-bold text-2xl text-blue-700 mb-3">Immediate Emotional Regulation</h3>
                    <p class="text-base text-gray-600 leading-relaxed">It facilitates in-the-moment calming exercises like **mindful breathing and sensory grounding** for managing acute anxiety.</p>
                </div>
                <div class="section-card p-6 bg-pink-50 border border-pink-200 hover:shadow-lg transition">
                    <h3 class="font-bold text-2xl text-pink-700 mb-3">Ethical and Empathetic Design</h3>
                    <p class="text-base text-gray-600 leading-relaxed">Safety is paramount. Amica's core logic includes **crisis detection filters** and always prioritizes non-judgmental, empathetic validation.</p>
                </div>
            </div>
        </section>

        <!-- 3. Chatbot (Personal Journey Section) -->
        <section id="chatbot-section" class="space-y-10 hidden">
            <h2 class="text-4xl font-bold text-center text-gray-800">Start Your Personal Journey with Amica</h2>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                <!-- Chat Interface (Visible) -->
                <div class="lg:col-span-2 section-card bg-white p-6 border border-gray-100">
                    <h3 class="text-2xl font-semibold text-indigo-600 mb-4">Your Private Chat Session</h3>
                    <div id="chat-window" class="chat-container mb-4 p-4 space-y-4">
                        <!-- Initial Message -->
                        <div class="flex justify-start">
                            <div class="amica-message p-3 rounded-xl rounded-tl-none shadow">
                                Welcome! I'm Amica, your mental wellness companion. How can I support you on your journey today? (Try something like, "I'm feeling overwhelmed.")
                            </div>
                        </div>
                    </div>
                    
                    <!-- Input and Send Button -->
                    <div class="flex space-x-3">
                        <input id="chat-input" type="text" placeholder="Type your message here... (e.g., 'I feel anxious today' or 'How do I start mindfulness?')" class="flex-grow p-3 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 shadow-sm" />
                        <button id="chat-send-button" class="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition duration-150 shadow-md">
                            Send
                        </button>
                    </div>
                </div>

                <!-- CIM Logic Trace (Personal Session Status) -->
                <div class="lg:col-span-1 section-card bg-gray-800 p-6 border border-gray-700">
                    <h3 class="text-2xl font-bold text-white mb-4 border-b border-indigo-400 pb-2">Personal Journey Status</h3>
                    <p class="text-gray-400 text-sm mb-4">
                        This panel reflects the live communication between your browser and Amica's Core Intelligence Module (CIM).
                    </p>
                    
                    <div class="mb-4">
                        <h4 class="text-lg font-semibold text-pink-400 mb-1">Amica's Dialogue Output</h4>
                        <div id="cim-dialogue-output" class="p-3 bg-gray-900 rounded-lg text-white font-medium text-sm italic min-h-[50px]">
                            Awaiting your first message...
                        </div>
                    </div>

                    <div>
                        <h4 class="text-lg font-semibold text-purple-400 mb-1">API Status & Action Command</h4>
                        <div id="cim-action-output" class="p-3 bg-gray-900 rounded-lg text-green-400 font-mono text-xs min-h-[50px] overflow-auto">
                            Idle: Ready_For_User_Input
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- 4. Team Member Biographies Section -->
        <section id="team" class="space-y-10 py-12">
            <h2 class="text-4xl font-bold text-center text-gray-800">Meet the Core Team</h2>
            <p class="text-center text-lg text-gray-600 max-w-3xl mx-auto">Amica was founded by a blend of clinical expertise and advanced AI engineering to ensure safety and effectiveness.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Team Member 1: Anurag Batham -->
                <div class="section-card bg-white p-6 border border-gray-100 text-center">
                    <div class="mx-auto h-60 w-60 bg-indigo-100 rounded-full flex items-center justify-center mb-4 overflow-hidden">
                        <!-- Path changed to assets/anurag.jpg -->
                        <img src="assets/Anurag.jpg" 
                             onerror="this.onerror=null; this.src='https://placehold.co/128x128/e0e7ff/4338ca?text=Anurag'"
                             alt="Profile photo of Anurag Batham" 
                             class="h-full w-full object-cover rounded-full">
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800"> Anurag Batham, B.Tech CSE</h3>
                    <p class="text-indigo-600 font-medium mb-3">Hardware & Systems Engineer</p>
                    <p class="text-gray-600">Anurag is a B.Tech CSE student specializing in embedded systems, IoT, and robotics. He is driven by a vision to create emotionally intelligent machines that can interact naturally with humans. At the project’s core, Anurag integrates hardware components — from microphones to servo motors — with real-time AI systems to bring the mental health support robot to life. His goal is to bridge the gap between AI empathy and physical interaction.</p>
                </div>
                
                <!-- Team Member 2: Hnin Lae Khaing -->
                <div class="section-card bg-white p-6 border border-gray-100 text-center">
                    <div class="mx-auto h-60 w-60 bg-pink-100 rounded-full flex items-center justify-center mb-4 overflow-hidden">
                        <!-- Path changed to assets/hnin.jpg -->
                        <img src="assets/Hnin.jpg" 
                             onerror="this.onerror=null; this.src='https://placehold.co/128x128/fce7f3/db2777?text=Hnin'"
                             alt="Profile photo of Hnin Lae Khaing" 
                             class="h-full w-full object-cover rounded-full">
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800">Hnin Lae Khaing, B.Tech CSE</h3>
                    <p class="text-pink-600 font-medium mb-3">AI & Frontend Lead</p>
                    <p class="text-gray-600">Hnin is a passionate B.Tech Computer Science student with a strong interest in artificial intelligence, human-computer interaction, and emotional well-being technology. She focuses on building empathetic AI models and user-friendly interfaces that make mental health support more accessible. As the AI and frontend lead, Hnin ensures the robot communicates with warmth and understanding, blending psychology and technology for real impact.</p>
                </div>
            </div>
        </section>
        
    </div>

    <!-- Footer -->
    <footer class="w-full bg-gray-900 mt-12 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-400">
            <p>&copy; 2025 Amica.ai. Clinically Informed. Ethically Designed.</p>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const chatInput = document.getElementById('chat-input');
            const sendButton = document.getElementById('chat-send-button');
            const chatWindow = document.getElementById('chat-window');
            const cimDialogueOutput = document.getElementById('cim-dialogue-output');
            const cimActionOutput = document.getElementById('cim-action-output');

            const appendMessage = (role, text) => {
                const isAmica = role === 'amica';
                const messageContainer = document.createElement('div');
                messageContainer.className = `flex ${isAmica ? 'justify-start' : 'justify-end'}`;
                
                const messageBubble = document.createElement('div');
                messageBubble.className = `p-3 rounded-xl shadow mt-2 ${isAmica ? 'amica-message rounded-tl-none' : 'user-message rounded-br-none'}`;
                // Use innerHTML to allow basic markdown formatting from Gemini
                messageBubble.innerHTML = text; 
                
                messageContainer.appendChild(messageBubble);
                chatWindow.appendChild(messageContainer);
                
                // Scroll to the bottom
                chatWindow.scrollTop = chatWindow.scrollHeight;
            };

            const processPrompt = async () => {
                const prompt = chatInput.value.trim();
                if (!prompt) return;

                // 1. UI Update (User Message)
                appendMessage('user', prompt);
                chatInput.value = ''; 
                
                sendButton.disabled = true;
                sendButton.textContent = 'Processing...';
                cimDialogueOutput.textContent = 'CIM is communicating with Amica\'s core intelligence...';
                cimActionOutput.textContent = 'Running API call...';

                try {
                    // 2. Call the Gemini API or Demo Fallback
                    const { response, actionCommand } = await window.callGeminiApi(prompt);
                    
                    // 3. Update History
                    window.USER_STATE.chat_history.push({ role: 'user', text: prompt });
                    window.USER_STATE.chat_history.push({ role: 'amica', text: response });
                    
                    // 4. UI Update (Amica Response)
                    appendMessage('amica', response);
                    cimDialogueOutput.innerHTML = `**Amica:** ${response.substring(0, 100)}...`;
                    cimActionOutput.textContent = actionCommand;

                } catch (error) {
                    console.error("Chat processing failed and fallback failed (should not happen):", error);
                    
                    // Fallback for a catastrophic failure
                    const criticalErrorMessage = 'A critical error occurred. Please refresh the page.';
                    appendMessage('amica', criticalErrorMessage);
                    cimDialogueOutput.textContent = `CRITICAL FAILURE: ${criticalErrorMessage}`;
                    cimActionOutput.textContent = `CRITICAL_ERROR: ${error.message}`; 
                } finally {
                    sendButton.disabled = false;
                    sendButton.textContent = 'Send';
                }
            };

            // Attach event listeners
            sendButton.addEventListener('click', processPrompt);

            // Optional: allow pressing Enter to submit
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    processPrompt();
                }
            });
        });
    </script>
</body>
</html>
v class="avatar-bot">A</div>', unsafe_allow_html=True)
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
