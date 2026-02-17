import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    # Model Configurations (Defaults to placeholders if keys not set)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    HF_TOKEN = os.getenv("HF_TOKEN")
    # RAG Settings
    RAG_KNOWLEDGE_PATH = DATA_DIR / "knowledge_base"
    
    # Output Settings
    VIDEO_Format = "mp4"
    IMAGE_Format = "png"

    @classmethod
    def ensure_directories(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.RAG_KNOWLEDGE_PATH.mkdir(parents=True, exist_ok=True)
        
        # Ensure keys are in os.environ for libraries that need them (like replicate)
        if cls.REPLICATE_API_TOKEN and cls.REPLICATE_API_TOKEN != "mock_token":
            os.environ["REPLICATE_API_TOKEN"] = cls.REPLICATE_API_TOKEN
        if cls.GROQ_API_KEY and cls.GROQ_API_KEY != "mock_key":
            os.environ["GROQ_API_KEY"] = cls.GROQ_API_KEY
        if cls.HF_TOKEN:
            os.environ["HF_TOKEN"] = cls.HF_TOKEN

Config.ensure_directories()
