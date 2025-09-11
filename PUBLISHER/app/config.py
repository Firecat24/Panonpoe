import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_MANUSCRIPTS = os.path.join(BASE_DIR, "app", "uploads", "manuscripts")
    UPLOAD_COVERS = os.path.join(BASE_DIR, "app", "uploads", "covers")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB