import mysql.connector
from mysql.connector import Error
from app.config import Config

class Database:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.connection and self.connection.is_connected():
            try:
                if exc_type is not None:
                    self.connection.rollback()
            finally:
                self.disconnect()

    def connect(self):
        if self.connection and self.connection.is_connected():
            return
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                autocommit=False,
            )

        except Error as e:
            print(f"❌ Error koneksi DB: {e}")
            self.connection = None
            raise

    def _ensure_connected(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()