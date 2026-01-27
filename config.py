import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Aetherium Genesis Configuration

# ความปลอดภัย
DESKTOP_PASSWORD = "Genesis_777"
MOBILE_PATTERN = "Z"  # สมมติว่าเป็นรูปตัว Z

# การจับจังหวะ (The Ritual)
KNOCK_TIMEOUT = 2.0   # เวลาสูงสุดระหว่างการเคาะแต่ละครั้ง (วินาที)
REQUIRED_KNOCKS = 3   # จำนวนครั้งที่ต้องเคาะ

# ประเภทอุปกรณ์เริ่มต้น
DEFAULT_DEVICE = "DESKTOP" # เปลี่ยนเป็น "MOBILE" ได้

# --- OAuth 2.0 Configuration ---
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "mock")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
