import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"))
    else:
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
except ImportError:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

class Config:
    GROQ_API_KEY = GROQ_API_KEY
    MODEL_NAME = MODEL_NAME
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found")
        print("✅ Configuration loaded!")
        print(f"✅ Using model: {cls.MODEL_NAME}")

if __name__ == "__main__":
    Config.validate()