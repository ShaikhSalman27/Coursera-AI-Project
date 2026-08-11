"""
modules/website_chat.py
--------------------------
Tavily se coursera.org par live search karna, aur us context se
security-guarded answer generate karna (source URLs ke saath).
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import tavily
from security_guard import MASTER_SYSTEM_PROMPT, response_validator


def search_coursera_website(question):
    """Run a Tavily web search restricted to coursera.org."""

    response = tavily.search(
        query=f"site:coursera.org {question}",
        max_results=5,
        search_depth="advanced"
    )

    if not response["results"]:
        return None

    context = ""
    source_urls = []

    for item in response["results"]:

        url = item["url"]

        context += f"""
        Title:
{       item['title']}

        Content:
        {item['content']}

        URL:
        {url}

        ---------------------------
        """
        source_urls.append(url)

    return {"context": context, "urls": source_urls}


def chat_with_website(question):
    """Answer a general Coursera question using live website search results."""

    website_data = search_coursera_website(question)

    if not website_data:
        return None

    website_context = website_data["context"]
    source_urls = website_data["urls"]

    # ------------------------
    # Setup modern LangChain components
    # ------------------------
    model = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)

    # --------------------------
    # Layer 3 - System Prompt
    # --------------------------
    prompt = ChatPromptTemplate.from_messages([
        ("system", MASTER_SYSTEM_PROMPT),
        (
            "human",
            """
            Website Context:
            {context}

            Question:
            {question}

            IMPORTANT INSTRUCTIONS:

            1. Answer the user's question using the provided Coursera
               website context.

            2. Do not invent information.

            3. Keep the answer clear and relevant.

            4. Do NOT create or modify URLs yourself.

            5. The source URLs will be attached programmatically
               after your answer.
            """
        )
    ])

    # Pure LCEL Chain Pipeline
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"context": website_context, "question": question})

    # --------------------------
    # Layer 4 - Response Validator
    # --------------------------
    validation = response_validator(question=question, context=website_context, answer=response)

    if validation["decision"] == "UNSAFE":
        return "❌ I couldn't provide a safe answer to this question."

    # -----------------------------------------
    # Attach Website Sources
    # -----------------------------------------
    sources_text = "\n\n### 🔗 Sources\n"

    for url in source_urls[:3]:
        sources_text += f"- {url}\n"

    return response + sources_text
