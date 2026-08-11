"""
modules/image_handler.py
--------------------------
Uploaded images se text/OCR + detailed visual explanation nikalta hai.
"""

from PIL import Image
import google.generativeai as genai


def get_image_text(uploaded_images):
    """Extract OCR text and a detailed description from uploaded images."""

    model = genai.GenerativeModel("gemini-3.5-flash")

    full_text = ""

    for file in uploaded_images:

        image = Image.open(file)

        prompt = """
        Analyze this image carefully.

        Extract:

        - All visible text (OCR)
        - Objects
        - Charts
        - Tables
        - Screenshots
        - UI elements
        - Graphs
        - Logos

        Give a detailed explanation.
        """

        response = model.generate_content([prompt, image])
        full_text += response.text + "\n"

    return full_text
