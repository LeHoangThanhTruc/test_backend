#Đây là nơi chuứa lệnh5 taạo cơ s3ở dưữ liệu
import sqlite3

DB_NAME = "database.db"

# Hàm lấy kết nối đến Database
def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Hàm khởi tạo bảng users khi khởi chạy ứng dụng
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()