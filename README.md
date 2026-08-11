# 🤖 Coursera AI Chatbot

Ek Streamlit-based AI chatbot jo PDF, Image, Video, aur Voice input samajh kar,
Coursera-related questions ka jawab deta hai — 4-layer security guard ke saath
(prompt-injection, off-topic questions, aur unsafe answers se protection).

## ✨ Features

- 📄 **PDF understanding** — text-layer PDFs ya scanned/image-based PDFs, dono
- 🖼️ **Image understanding** — OCR + charts/tables/UI explanation
- 🎥 **Video understanding** — full transcript, timestamps, scene description, OCR
- 🎙️ **Voice input** — English / Hindi / Hinglish speech-to-text
- 🌐 **Live website search** — coursera.org se real-time answers (Tavily)
- 🛡️ **4-layer Security Guard** — Question Guard → Context Guard → System Prompt → Response Validator

## 📁 Project Structure

```
coursera-ai-chatbot/
├── CourseraAIChatbot.py     # Main Streamlit app (UI + orchestration)
├── config.py                # Gemini + Tavily API key setup
├── security_guard.py        # 4-layer security guard logic
├── modules/
│   ├── pdf_handler.py       # PDF text extraction
│   ├── image_handler.py     # Image OCR + analysis
│   ├── video_handler.py     # Video analysis
│   ├── voice_handler.py     # Voice-to-text
│   ├── vector_store.py      # Chunking + FAISS vector store
│   ├── pdf_chat.py          # Chat over uploaded content
│   └── website_chat.py      # Chat over live Coursera website search
├── requirements.txt
├── .env.example
└── .gitignore
```

## ⚙️ Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/coursera-ai-chatbot.git
   cd coursera-ai-chatbot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   ```bash
   cp .env.example .env
   # .env file kholkar apni GOOGLE_API_KEY aur TAVILY_API_KEY daal do
   ```

4. Run the app:
   ```bash
   python -m streamlit run app.py
   ```

## 🔑 Getting API Keys

- **Google Gemini API Key** — https://aistudio.google.com/app/apikey
- **Tavily API Key** — https://tavily.com

## 🛡️ Security Layers (`security_guard.py`)

| Layer | Purpose |
|-------|---------|
| Question Guard | User ka sawaal Coursera-related hai ya nahi, check karta hai |
| Context Guard | Retrieved content official Coursera source se hai ya nahi |
| Master System Prompt | Model ko role/behaviour se bandh ke rakhta hai |
| Response Validator | Final answer safe aur relevant hai ya nahi, verify karta hai |

## 📜 License

MIT
