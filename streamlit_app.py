# --- CUSTOM CSS ---
st.markdown("""
<style>
/* CHANGED: Background color to sky blue */
[data-testid="stAppViewContainer"] {
    background-color: #87CEEB; /* Sky Blue */
    background-image: none; /* Removed gradient to ensure solid color */
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
/* CHANGED: Header color to black for readability on new background */
h1 { color: Black; text-align: center; } 
[data-testid="stWarning"] {
    background-color: black;
    border-radius: 15px;
    border-color: #3b82f6;
    /* CHANGED: Warning text color to blue for readability */
    color: blue; 
}
</style>
""", unsafe_allow_html=True)
