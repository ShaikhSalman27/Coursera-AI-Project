"""
config.py
----------
Central place for API key setup (Gemini + Tavily).
Har module isi file se `api_key` aur `tavily` import karega,
taaki key sirf ek jagah configure ho.
"""

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from tavily import TavilyClient

# ----------------------------
# Load local .env file (only for local development)
# ----------------------------
load_dotenv()

# ----------------------------
# Google Gemini API Key
# ----------------------------
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.error("Google API Key not found. Please configure GOOGLE_API_KEY.")
    st.stop()

# Configure Gemini globally
genai.configure(api_key=api_key)

# ----------------------------
# Tavily API Key
# ----------------------------
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    tavily_api_key = st.secrets["TAVILY_API_KEY"]

tavily = TavilyClient(api_key=tavily_api_key)
