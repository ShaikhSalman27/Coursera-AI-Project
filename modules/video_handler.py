"""
modules/video_handler.py
---------------------------
Uploaded video ko Gemini par upload karke, poori video ka transcript,
scene description, OCR, charts, key-points, summary nikalta hai.
"""

import os
import time
import tempfile
import streamlit as st
from google import genai as genai_client

from config import api_key


VIDEO_ANALYSIS_PROMPT = """
You are an expert AI Video Analyzer.

Watch the COMPLETE video carefully from beginning to end.

Your task is to analyze everything present in the video.

====================================================
1. COMPLETE TRANSCRIPT
====================================================

Generate the complete spoken transcript.

Include:

- Every spoken sentence
- Speaker changes if identifiable
- Conversations
- Narration
- Voice-over
- Background announcements

Do not skip any dialogue.

====================================================
2. TIMESTAMP-WISE BREAKDOWN
====================================================

Divide the video into chronological sections.

For each important timestamp include:

Timestamp:
What is happening?
Who is speaking?
Important discussion.

Example:

00:00 - Introduction

02:15 - Python Variables

05:42 - Function Example

08:10 - Summary

====================================================
3. SCENE DESCRIPTION
====================================================

Describe every important scene.

Include:

- Environment
- People
- Objects
- Actions
- Camera changes
- Demonstrations
- Screen recordings

====================================================
4. OCR (VISIBLE TEXT)
====================================================

Extract ALL visible text appearing in the video.

Include text from:

- Slides
- Screens
- Whiteboards
- Documents
- UI
- Presentations
- Captions
- Labels
- Titles

Do not miss any readable text.

====================================================
5. TABLES
====================================================

If tables appear,

Explain:

- Headers
- Rows
- Columns
- Values
- Meaning

====================================================
6. CHARTS & GRAPHS
====================================================

If charts appear,

Explain:

- Chart type
- Axes
- Data
- Trend
- Conclusions

====================================================
7. SCREENSHOTS / UI
====================================================

If software is shown,

Describe:

- Buttons
- Menus
- Windows
- Forms
- Settings
- Navigation
- Workflow

====================================================
8. OBJECT DETECTION
====================================================

Identify important objects.

Examples:

Laptop

Phone

Book

Person

Machine

Vehicle

Equipment

Tools

====================================================
9. IMPORTANT EVENTS
====================================================

List all important events occurring during the video.

====================================================
10. STEP-BY-STEP ACTIONS
====================================================

If the video is a tutorial,

Write every step in order.

====================================================
11. KEY POINTS
====================================================

Extract all important concepts.

====================================================
12. SUMMARY
====================================================

Generate:

* Short Summary

* Detailed Summary

====================================================
13. QUESTIONS THAT CAN BE ANSWERED
====================================================

List important topics covered so users can ask questions later.

====================================================
14. FINAL NOTES
====================================================

Return everything in clean Markdown format using headings and bullet points.

Never skip important information.

Be as detailed as possible.
"""


def get_video_text(uploaded_videos):
    """Upload each video to Gemini and return a detailed markdown analysis."""

    client = genai_client.Client(api_key=api_key)

    full_text = ""

    for file in uploaded_videos:

        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(file.read())
            temp_path = temp_video.name

        # Upload to Gemini
        video_file = client.files.upload(file=temp_path)

        # Wait until processed
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = client.files.get(name=video_file.name)

        if video_file.state.name == "FAILED":
            st.error("Video Processing Failed")
            os.remove(temp_path)  # cleanup even on failure
            continue

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[VIDEO_ANALYSIS_PROMPT, video_file]
        )

        full_text += response.text + "\n"

        os.remove(temp_path)

    return full_text
