"""
CourseraAIChatbot.py
--------
Main Streamlit entrypoint.

Sirf yeh file UI aur flow control karti hai — actual "logic"
alag-alag modules/ files me hai (PDF, image, video, voice, vector-store,
pdf-chat, website-chat), aur security saari security_guard.py me hai.

Run:
    python -m streamlit run CourseraAIChatbot.py
"""

import os
import streamlit as st

from config import api_key  # noqa: F401  (ensures Gemini + Tavily are configured on import)

from modules.pdf_handler import get_pdf_text
from modules.image_handler import get_image_text
from modules.video_handler import get_video_text
from modules.voice_handler import voice_to_text
from modules.vector_store import get_text_chunks, get_vector_store
from modules.pdf_chat import chat_with_pdf
from modules.website_chat import chat_with_website

from security_guard import question_guard, query_router
from modules.ui_theme import inject_custom_css, render_header


# ------------------------
# Streamlit Web Interface
# ------------------------
st.set_page_config(
    page_title="Coursera AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

inject_custom_css()
render_header()

# Avatars used consistently across every chat bubble
AVATARS = {"user": "🧑‍💻", "assistant": "🤖"}

# Sidebar: File Upload Section
with st.sidebar:

    st.markdown("### 📂 Upload Documents")
    # st.caption("PDF, image ya video daalo — phir 'Process Files' dabao.")

    uploaded_pdfs = st.file_uploader(
        "📄 PDF Files",
        type="pdf",
        accept_multiple_files=True
    )

    uploaded_images = st.file_uploader(
        "🖼️ Images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True
    )

    uploaded_videos = st.file_uploader(
        "🎥 Videos",
        type=["mp4", "mov", "avi", "mkv"],
        accept_multiple_files=True
    )

    st.markdown("")

    if st.button("⚡ Process Files"):

        with st.spinner("Processing..."):

            raw_text = ""

            if uploaded_pdfs:
                raw_text += get_pdf_text(uploaded_pdfs)

            if uploaded_images:
                raw_text += get_image_text(uploaded_images)

            if uploaded_videos:
                raw_text += get_video_text(uploaded_videos)

            chunks = get_text_chunks(raw_text)
            get_vector_store(chunks)

            st.success("✅ Files Processed Successfully")


# Persistent Chat History Configuration
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display active historical messages instantly on redraw
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=AVATARS.get(message["role"])):
        st.markdown(message["content"])

# -------------------------------------------------
# User prompt interaction
# Supports both Text + Voice
# -------------------------------------------------
user_input = st.chat_input(
    "💬 Ask your question...",
    accept_audio=True,
    audio_sample_rate=16000,
    key="main_chat_input"
)

user_question = None

# -----------------------------------------
# Text Question
# -----------------------------------------
if user_input:

    if user_input.text:
        user_question = user_input.text.strip()

    # -----------------------------------------
    # Voice Question
    # -----------------------------------------
    elif user_input.audio:

        with st.spinner("🎙️ Understanding your question..."):
            user_question = voice_to_text(user_input.audio)

        if user_question:
            st.info(f"🎙️ You asked: {user_question}")


# -----------------------------------------
# Continue Existing Chatbot Logic
# -----------------------------------------
if user_question:

    # --------------------------
    # Layer 1 - Question Guard
    # --------------------------
    guard = question_guard(user_question)

    # --------------------------
    # Greeting -> reply directly, skip router
    # --------------------------
    if guard["decision"] == "GREETING":

        with st.chat_message("user", avatar=AVATARS["user"]):
            st.markdown(user_question)

        st.session_state.messages.append({"role": "user", "content": user_question})

        greeting_reply = guard.get(
            "reply",
            "Hello! 👋 I'm your Coursera AI Assistant. Ask me anything about Coursera."
        )

        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            st.markdown(greeting_reply)

        st.session_state.messages.append({"role": "assistant", "content": greeting_reply})

        st.stop()

    if guard["decision"] == "DENY":
        st.warning("❌ I can only answer Coursera-related questions.")
        st.stop()

    # --------------------------
    # Query Router
    # --------------------------
    route = query_router(user_question)

    # --------------------------
    # Reject
    # --------------------------
    if route["route"] == "REJECT":
        st.warning("❌ I can only answer Coursera-related questions.")
        st.stop()

    # --------------------------------
    # Render and store user message
    # --------------------------------
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(user_question)

    st.session_state.messages.append({"role": "user", "content": user_question})

    # --------------------------------
    # Generate Assistant Response
    # --------------------------------
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):

        with st.spinner("Analyzing context..."):

            try:
                # --------------------------
                # PDF Route
                # --------------------------
                if route["route"] == "PDF":

                    if not os.path.exists("pass_index"):
                        st.warning("❌ No uploaded content is available.")
                        st.stop()

                    pdf_result = chat_with_pdf(user_question)
                    answer = pdf_result["answer"]

                # --------------------------
                # Website Route
                # --------------------------
                elif route["route"] == "WEBSITE":

                    answer = chat_with_website(user_question)

                    if not answer:
                        st.warning("❌ I couldn't find relevant information on Coursera.")
                        st.stop()

                # --------------------------
                # Display Answer
                # --------------------------
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                st.error(f"Error executing search query: {str(e)}")
