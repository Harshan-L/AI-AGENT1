import streamlit as st

from main import ask_gemini


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Harshan's AI Agent",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Harshan's AI Agent")

    st.write(
        "An AI assistant powered by Gemini "
        "with external search tools."
    )

    st.divider()

    st.subheader("🛠️ Available Tools")

    st.write("📚 Wikipedia")
    st.write("🌐 DuckDuckGo Web Search")

    st.divider()

    st.subheader("💡 What I Can Do")

    st.write("• Answer general questions")
    st.write("• Search Wikipedia")
    st.write("• Search the web")
    st.write("• Remember the current conversation")

    st.divider()

    # ========================================================
    # CLEAR CHAT BUTTON
    # ========================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# INITIALIZE CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🤖 Harshan's AI Agent")

st.caption(
    "Gemini + Wikipedia + DuckDuckGo Web Search"
)


st.write(
    "Ask questions, search the web, and have a conversation "
    "with an AI assistant."
)


# ============================================================
# WELCOME MESSAGE
# ============================================================

if len(st.session_state.messages) == 0:

    st.info(
        "👋 Welcome! I'm your AI Agent. "
        "Ask me anything or try one of the examples below."
    )

    st.subheader("💡 Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write("📚 **Knowledge**")

        st.write(
            "Who invented the telephone?"
        )

    with col2:

        st.write("🌐 **Web Search**")

        st.write(
            "What are the latest developments in AI?"
        )

    with col3:

        st.write("💻 **Programming**")

        st.write(
            "Explain Java HashMap."
        )


# ============================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Type your question..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input:

    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.write(user_input)


    # --------------------------------------------------------
    # CREATE CONVERSATION HISTORY
    # --------------------------------------------------------

    conversation = ""

    for message in st.session_state.messages:

        role = message["role"]
        content = message["content"]

        if role == "user":

            conversation += (
                f"User: {content}\n"
            )

        elif role == "assistant":

            conversation += (
                f"Assistant: {content}\n"
            )


    # --------------------------------------------------------
    # GET AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                answer = ask_gemini(
                    conversation
                )

                st.write(answer)

                # ------------------------------------------------
                # SAVE AI RESPONSE
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )