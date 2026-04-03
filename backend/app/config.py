import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    # Para menos latencia en OpenRouter probá: google/gemini-2.0-flash-001 o openai/gpt-4o-mini
    DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")

settings = Settings()