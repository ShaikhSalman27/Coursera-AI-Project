"""
modules/voice_handler.py
---------------------------
Recorded audio (chat_input ka mic) ko Gemini se transcribe karta hai
(English / Hindi / Hinglish support ke saath).
"""

import os
import tempfile
import streamlit as st
from google import genai as genai_client

from config import api_key


VOICE_TRANSCRIBE_PROMPT = """
Listen to the user's audio carefully.

Convert the speech into text.

Requirements:

- Support English.
- Support Hindi.
- Support Hinglish.
- Preserve the original meaning.
- Correct obvious speech recognition mistakes.
- Do NOT answer the question.
- Return ONLY the transcribed question.
- Do not add explanations.

Example:

Audio:
"when was coursera launched"

Output:
When was Coursera launched?
"""


def voice_to_text(audio_file):
    """Transcribe a recorded audio blob into text using Gemini."""

    temp_audio_path = None

    try:
        # Save recorded audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_file.getvalue())
            temp_audio_path = temp_audio.name

        # Use NEW Google GenAI SDK
        client = genai_client.Client(api_key=api_key)

        # Upload audio using new SDK
        uploaded_audio = client.files.upload(file=temp_audio_path)

        # Ask Gemini to transcribe the audio
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[VOICE_TRANSCRIBE_PROMPT, uploaded_audio]
        )

        return response.text.strip()

    except Exception as e:
        st.error(f"Voice processing error: {str(e)}")
        return None

    finally:
        # Cleanup temporary file
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
