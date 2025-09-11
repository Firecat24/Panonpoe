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
            
    # -------------------------
    # Fungsi CRUD untuk naskah
    # -------------------------
    def add_manuscript(self, title, author_name, author_email, synopsis, manuscript_file):
        cur = self.connection.cursor()
        cur.execute(
            """INSERT INTO manuscripts(title, author_name, author_email, synopsis, manuscript_file, status)
               VALUES(%s, %s, %s, %s, %s, 'DIAJUKAN')""",
            (title, author_name, author_email, synopsis, manuscript_file)
        )
        self.connection.commit()
        mid = cur.lastrowid
        cur.close()
        return mid

    def list_manuscripts(self):
        cur = self.connection.cursor(dictionary=True)
        cur.execute("""SELECT id, title, author_name, status, created_at 
                       FROM manuscripts ORDER BY created_at DESC""")
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_manuscript(self, manuscript_id):
        cur = self.connection.cursor(dictionary=True)
        cur.execute("SELECT * FROM manuscripts WHERE id=%s", (manuscript_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def update_status(self, manuscript_id, new_status):
        cur = self.connection.cursor()
        cur.execute("UPDATE manuscripts SET status=%s WHERE id=%s", (new_status, manuscript_id))
        self.connection.commit()
        cur.close()

    def update_cover(self, manuscript_id, cover_file):
        cur = self.connection.cursor()
        cur.execute("UPDATE manuscripts SET cover_file=%s WHERE id=%s", (cover_file, manuscript_id))
        self.connection.commit()
        cur.close()