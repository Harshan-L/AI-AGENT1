import streamlit as st
from main import ask_gemini

st.set_page_config(
    page_title="My AI Agent",
    page_icon="🤖"
)

st.title("🤖 My AI Agent")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your question...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer = ask_gemini(user_input)

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Error: {e}")