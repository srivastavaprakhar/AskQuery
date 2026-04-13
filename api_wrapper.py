from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from main import suppress_output
from main import answer_question, safe_llm_init
from embed_and_index import build_index
import logging
import os
from fastapi.middleware.cors import CORSMiddleware

# ✅ NEW IMPORTS
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
# ✅ IMPORT CONFIG
from config import SUPABASE_URL

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# ==============================
# 🔐 SUPABASE AUTH CONFIG
# ==============================
SUPABASE_JWKS_URL = f"{SUPABASE_URL}/auth/v1/keys"
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # 🔥 Use Supabase Auth API instead of manual JWT decode
        res = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": SUPABASE_ANON_KEY
            }
        )

        if res.status_code != 200:
            raise Exception("Invalid token")

        user = res.json()
        return user

    except Exception as e:
        print("AUTH ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
# ==============================
# 🔧 LOGGING SETUP
# ==============================
logging.getLogger("watchdog").setLevel(logging.WARNING)

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()

# ==============================
# 🚀 FASTAPI APP
# ==============================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 🧠 LOAD MODEL + INDEX
# ==============================
with suppress_output():
    model = safe_llm_init()
    index = build_index()

# ==============================
# 📦 REQUEST MODEL
# ==============================
class QuestionRequest(BaseModel):
    question: str


# ==============================
# 🧪 HEALTH CHECK
# ==============================
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ==============================
# 🔐 SECURED ENDPOINT
# ==============================
@app.post("/ask")
def api_ask(
    req: QuestionRequest,
    user=Depends(verify_token)
):
    try:
        user_email = user.get("email", "unknown")

        logger.info(f"[USER: {user_email}] Question: {req.question}")

        response = answer_question(index, req.question, model)

        logger.info(f"[USER: {user_email}] Response: {response}")

        return {"answer": response}

    except Exception:
        logger.exception("Error while answering question.")
        raise HTTPException(status_code=500, detail="Error generating response")


# ==============================
# ▶️ RUN SERVER
# ==============================
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "api_wrapper:app",
        host="0.0.0.0",   # 🔥 IMPORTANT
        port=port
    )