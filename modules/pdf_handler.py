"""
modules/pdf_handler.py
------------------------
PDF se text extract karne ka function.
Pehle normal text-layer try karta hai, agar text nahi milta
(scanned PDF) to Gemini Vision se page-by-page image analysis karta hai.
"""

import io
import fitz  # PyMuPDF
from PIL import Image
from PyPDF2 import PdfReader
import google.generativeai as genai


def get_pdf_text(uploaded_files):
    """Extract text (and describe tables/charts/images) from uploaded PDFs."""

    model = genai.GenerativeModel("gemini-3.5-flash")

    full_text = ""

    for file in uploaded_files:

        # ----------------------------
        # First Try Normal Text
        # ----------------------------
        file.seek(0)
        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        # ----------------------------
        # If Text Found
        # ----------------------------
        if len(text.strip()) > 100:
            full_text += text
            continue

        # ----------------------------
        # Otherwise Scan Images (scanned / image-based PDF)
        # ----------------------------
        file.seek(0)
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        for page in pdf:

            pix = page.get_pixmap(dpi=250)
            image = Image.open(io.BytesIO(pix.tobytes("png")))

            prompt = """
            You are reading a PDF page.

            Extract ALL readable text.

            Also explain:

            - Tables
            - Charts
            - Flow diagrams
            - Screenshots
            - Images

            Return everything in proper readable format.
            """

            response = model.generate_content([prompt, image])
            full_text += response.text + "\n"

    return full_text
