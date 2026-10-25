from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Tạo database và bảng users tự động
def init_db():
    conn = sqlite3.connect("database.db")
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

init_db()

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# 1. API Đăng ký
@app.post("/api/auth/register")
def register(data: RegisterRequest):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
            (data.full_name, data.email, data.password)
        )
        conn.commit()
        return {"status": "success", "message": "Đăng ký thành công!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng!")
    finally:
        conn.close()

# 2. API Đăng nhập
@app.post("/api/auth/login")
def login(data: LoginRequest):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, full_name, email FROM users WHERE email = ? AND password_hash = ?",
        (data.email, data.password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "status": "success",
            "message": "Đăng nhập thành công!",
            "user": {
                "id": user[0],
                "full_name": user[1],
                "email": user[2]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Sai email hoặc mật khẩu!")