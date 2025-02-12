import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DEFAULT_LLM = None

if os.getenv("LLM_PROVIDER") == "google":
    DEFAULT_LLM = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        api_key=os.getenv("GEMINI_API_KEY"), 
        temperature=0
    )
elif os.getenv("LLM_PROVIDER") == "openai":
    DEFAULT_LLM = ChatOpenAI(
        model="gpt-4o-mini", 
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )
else:
    raise ValueError("Invalid LLM_PROVIDER")

__all__ = [DEFAULT_LLM]