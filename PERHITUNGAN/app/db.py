import mysql.connector
from mysql.connector import Error
from app import app

# Fungsi untuk koneksi ke database MySQL
def koneksi_database():
    return mysql.connector.connect(
        host="localhost", 
        user="Firecat243121", 
        password="Ikanissakana123!", 
        database="falak"
    )