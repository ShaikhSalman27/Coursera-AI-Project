"""
modules/ui_theme.py
----------------------
Coursera-brand-inspired visual theme for the Streamlit app.

Sirf visual layer hai — koi business logic yahan nahi.
`inject_custom_css()` aur `render_header()` ko app.py ke top par call karo.
"""

import streamlit as st


def inject_custom_css():
    """Inject the full custom stylesheet (fonts, colors, chat bubbles, sidebar, etc.)."""

    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        :root {
            --navy: #041E42;
            --navy-light: #0A2E5C;
            --blue: #0056D2;
            --blue-light: #2E7CF6;
            --bg: #F4F8FF;
            --card: #FFFFFF;
            --border: #D8E3F0;
            --text: #1A1A2E;
            --muted: #5B6B82;
            --success: #00A67E;
        }

        /* ---------------------------------- */
        /* Global                              */
        /* ---------------------------------- */

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--bg);
        }

        h1, h2, h3, h4 {
            font-family: 'Poppins', sans-serif !important;
            # color: var(--navy) !important;
        }

        #MainMenu, footer, header[data-testid="stHeader"] {
            background: transparent;
        }

        /* ---------------------------------- */
        /* Custom Top Banner                   */
        /* ---------------------------------- */

        .coursera-hero {
            background: linear-gradient(120deg, var(--navy) 0%, var(--blue) 100%);
            border-radius: 18px;
            padding: 28px 32px;
            margin-bottom: 22px;
            box-shadow: 0 10px 30px rgba(4, 30, 66, 0.25);
        }

        .coursera-hero h1 {
            color: #FFFFFF !important;
            font-size: 1.8rem;
            margin: 0 0 4px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .coursera-hero p {
            color: #CFE0FF;
            margin: 0;
            font-size: 0.95rem;
        }

        .trust-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
        }

        .trust-chip {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #FFFFFF;
            font-size: 0.75rem;
            font-weight: 500;
            padding: 5px 12px;
            border-radius: 999px;
            backdrop-filter: blur(4px);
        }

        /* ---------------------------------- */
        /* Sidebar                             */
        /* ---------------------------------- */

        section[data-testid="stSidebar"] {
            background: var(--navy);
        }

        /* Only these elements turn light — NOT a blanket "*" rule,
           so it can never fight with the upload button's own colors below */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #E8F0FE;
        }

        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] * {
            color: #E8F0FE !important;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-family: 'Poppins', sans-serif;
            color: #FFFFFF;
        }

        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background: var(--navy-light);
            border: 1.5px dashed rgba(255, 255, 255, 0.35);
            border-radius: 12px;
        }

        /* "Browse files" / "Upload" button inside the uploader — Streamlit
           keeps this white, so it needs its own explicit navy-on-white
           colors, set on every descendant (icon + text) with high priority */
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
            background-color: #FFFFFF !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button *,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button * {
            color: var(--navy) !important;
            fill: var(--navy) !important;
            stroke: var(--navy) !important;
            opacity: 1 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button:hover * {
            background-color: #EAF1FF !important;
            color: var(--blue) !important;
            fill: var(--blue) !important;
            stroke: var(--blue) !important;
        }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
            background: linear-gradient(120deg, var(--blue) 0%, var(--blue-light) 100%);
            color: #FFFFFF !important;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 4px 14px rgba(0, 86, 210, 0.35);
            transition: transform 0.15s ease;
        }

        section[data-testid="stSidebar"] .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(0, 86, 210, 0.45);
        }

        /* ---------------------------------- */
        /* Chat bubbles                        */
        /* ---------------------------------- */

        [data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 4px 6px;
            margin-bottom: 10px;
            border: none !important;
            box-shadow: 0 2px 10px rgba(4, 30, 66, 0.06);
        }

        /* User message (right-leaning, blue) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            background: linear-gradient(120deg, var(--blue) 0%, var(--blue-light) 100%);
            margin-left: 12%;
        }

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span {
            color: #FFFFFF !important;
        }

        /* Assistant message (left-leaning, white card) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
            background: var(--card);
            border-left: 4px solid var(--blue) !important;
            margin-right: 12%;
        }

        /* ---------------------------------- */
        /* Chat input                          */
        /* ---------------------------------- */

        [data-testid="stChatInput"] {
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(4, 30, 66, 0.12);
        }

        /* ---------------------------------- */
        /* Alerts (success / warning / error)  */
        /* ---------------------------------- */

        div[data-testid="stAlert"] {
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render the Coursera-brand hero banner with a security trust-badge row."""

    st.markdown(
        """
        <div class="coursera-hero">
            <h1>🤖 Coursera AI Assistant</h1>
            <p>Ask about courses, certificates, pricing — or chat with your uploaded PDFs, images &amp; videos.</p>
            <div class="trust-row">
                <span class="trust-chip">🛡️ Question Guard</span>
                <span class="trust-chip">📚 Context Guard</span>
                <span class="trust-chip">🧭 Guided Responses</span>
                <span class="trust-chip">✅ Response Validator</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
