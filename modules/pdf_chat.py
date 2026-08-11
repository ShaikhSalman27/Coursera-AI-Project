"""
modules/pdf_chat.py
----------------------
Uploaded content (PDF/image/video ka processed text) ke FAISS index
me se relevant chunks dhundh kar, security-guarded answer generate karta hai.
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from security_guard import context_guard, MASTER_SYSTEM_PROMPT, response_validator


def chat_with_pdf(question):
    """Answer a question using the locally stored FAISS index (uploaded content)."""

    # Load local vector database
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = FAISS.load_local("pass_index", embeddings, allow_dangerous_deserialization=True)

    # Retrieve relevant document snippets
    docs = db.similarity_search_with_score(question, k=3)

    # Merge document text blocks into a single context string
    context_text = "\n\n".join([doc.page_content for doc, score in docs])

    # --------------------------
    # Layer 2 - Context Guard
    # --------------------------
    guard = context_guard(question=question, context=context_text)

    if guard["decision"] == "DENY":
        return {
            "found": False,
            "answer": "❌ The uploaded content is not related to Coursera."
        }

    # --------------------------
    # Setup modern LangChain components
    # --------------------------
    model = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)

    # --------------------------
    # Layer 3 - System Prompt
    # --------------------------
    prompt = ChatPromptTemplate.from_messages([
        ("system", MASTER_SYSTEM_PROMPT),
        (
            "human",
            """
            Context:
            {context}

            Question:
            {question}

            """
        )
    ])

    # Pure LCEL Chain Pipeline
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"context": context_text, "question": question})

    # --------------------------
    # Layer 4 - Response Validator
    # --------------------------
    validation = response_validator(question=question, context=context_text, answer=response)

    if validation["decision"] == "UNSAFE":
        return {
            "found": False,
            "answer": "❌ I couldn't provide a safe answer to this question."
        }

    return {"found": True, "answer": response}
