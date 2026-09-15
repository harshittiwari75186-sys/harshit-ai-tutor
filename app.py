model = genai.GenerativeModel("models/gemini-1.5-flash")
import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Harshit AI Tutor",
    page_icon="🎓",
    layout="centered"
)

# 2. Get API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY नहीं मिली! कृपया Streamlit Secrets में GEMINI_API_KEY सेट करें।")
    st.stop()

# 3. Configure Gemini AI
genai.configure(api_key=api_key)

# 4. Initialize Model (Using explicit model string)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 5. App UI Header
st.title("🎓 Harshit AI Tutor")
st.caption("Learn English • Speak Confidently • Practice Daily")
st.write("Created by **Harshit Tiwari**")
st.divider()

# 6. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": ["Hello! I'm your AI English Tutor. Ask me anything about grammar, vocabulary, sentence formation, or daily speaking practice!"]
        }
    ]

# 7. Display Chat History
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["parts"][0])

# 8. User Input and Gemini Response
if prompt := st.chat_input("Type your question in English or Hindi..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})

    try:
        with st.spinner("Thinking..."):
            chat = model.start_chat(history=st.session_state.messages[:-1])
            response = chat.send_message(prompt)
            
            with st.chat_message("assistant"):
                st.write(response.text)
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        st.error(f"Error occurred: {e}")
