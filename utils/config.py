import os
from dotenv import load_dotenv

# Load from .env for local development
load_dotenv()

# Check if running on Streamlit Cloud
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Running on Streamlit Cloud - use secrets
        GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY"))
        MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"))
    else:
        # Running locally - use .env
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
except ImportError:
    # Streamlit not installed - use .env
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

class Config:
    GROQ_API_KEY = GROQ_API_KEY
    TAVILY_API_KEY = TAVILY_API_KEY
    MODEL_NAME = MODEL_NAME
    TEMPERATURE = 0.7
    MAX_TOKENS = 4000
    
    @classmethod
    def validate(cls):
        """Validate that all required keys are present"""
        if not cls.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found in environment")
        if not cls.TAVILY_API_KEY:
            raise ValueError("❌ TAVILY_API_KEY not found in environment")
        print("✅ Configuration loaded successfully!")
        print(f"✅ Using model: {cls.MODEL_NAME}")

if __name__ == "__main__":
    Config.validate()