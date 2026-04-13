import os
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")

# Optional local model path (not required for Gemini cloud API)
MODEL_PATH = os.getenv("MODEL_PATH", "")
SUPABASE_DB_HOST = "aws-1-ap-northeast-2.pooler.supabase.com"
SUPABASE_DB_NAME = "postgres"
SUPABASE_DB_USER = "postgres.nkkmvtkvozkboelcabkj"
SUPABASE_DB_PASSWORD = DB_PASSWORD
SUPABASE_DB_PORT = 6543
SUPABASE_URL="https://nkkmvtkvozkboelcabkj.supabase.co"
# Use GEMINI_API_KEY for Google Gemini access
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")