import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Harshit AI Tutor",
    page_icon="🎓",
    layout="centered",
)

SYSTEM_PROMPT = """
You are Harshit AI Tutor, an English-learning assistant created by Harshit Tiwari.

Your purpose is to help learners improve English speaking, grammar, vocabulary,
daily conversation, and B1 interview communication.

Teaching rules:
1. Use clear, practical English.
2. Support Hindi explanations when the learner asks for Hindi.
3. Correct important grammar mistakes politely and simply.
4. Encourage complete sentences.
5. During speaking/interview practice, ask one question at a time.
6. Encourage reasons and examples when appropriate.
7. Gradually increase difficulty from beginner to B1/B2.
8. Do not claim to provide an official CEFR certification. If estimating level,
   call it an "AI practice estimate".
9. Be supportive but honest; do not give exaggerated praise.
10. When correcting English, show the corrected sentence and briefly explain why.
"""

st.title("🎓 Harshit AI Tutor")
st.caption("Learn English • Speak confidently • Believe in yourself")
st.write("**Created by Harshit Tiwari**")

# Create the OpenAI client from Streamlit Secrets.
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error(
        "OPENAI_API_KEY is not configured yet. "
        "After deploying, add it in Streamlit → App settings → Secrets."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info(
        "👋 Hello! I'm Harshit AI Tutor. "
        "Ask me about English grammar, vocabulary, speaking practice, "
        "daily conversation, or B1 interview preparation."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your English question here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Send recent conversation context to the model.
    recent_messages = st.session_state.messages[-12:]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.responses.create(
                    model="gpt-5.6-luna",
                    instructions=SYSTEM_PROMPT,
                    input=recent_messages,
                )
                answer = response.output_text
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(
                    "I couldn't connect to the AI service. "
                    "Please check your API key and try again."
                )
                st.caption(f"Technical detail: {e}")

with st.sidebar:
    st.header("📚 Practice Modes")
    st.write("🗣️ Speaking Practice")
    st.write("✍️ Grammar")
    st.write("📖 Vocabulary")
    st.write("🎤 B1 Interview")
    st.write("💬 Daily Conversation")
    st.write("🇮🇳 Hindi → English")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Harshit AI Tutor")
    st.caption("Created by Harshit Tiwari")
