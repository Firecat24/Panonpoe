import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")  # untuk session/flash
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "publisher")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_MANUSCRIPTS = os.path.join(BASE_DIR, "app", "uploads", "manuscripts")
    UPLOAD_COVERS = os.path.join(BASE_DIR, "app", "uploads", "covers")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB