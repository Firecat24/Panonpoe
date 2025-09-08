import mysql.connector
from mysql.connector import Error
from app.config import Config

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if self.connection.is_connected():
                print(f"✅ Koneksi berhasil ke database {Config.DB_NAME}")
        except Error as e:
            print(f"❌ Error koneksi DB: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Koneksi ditutup")