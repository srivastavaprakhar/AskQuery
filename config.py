import os
from dotenv import load_dotenv

load_dotenv()

# Optional local model path (not required for Gemini cloud API)
MODEL_PATH = os.getenv("MODEL_PATH", "")
DB_PATH = "database/trial1.db"
INDEX_PATH = "faiss_index"

# Use GEMINI_API_KEY for Google Gemini access
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")