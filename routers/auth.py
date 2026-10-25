#Đây là file  logic code từng chức năng. Ở đây là đăng ký đăng nhập
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from database import get_db

# Khởi tạo APIRouter thay vì FastAPI()
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# Struct nhận dữ liệu
class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# 1. API Đăng ký (/api/auth/register)
@router.post("/register")
def register(data: RegisterRequest):
    conn = get_db()
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

# 2. API Đăng nhập (/api/auth/login)
@router.post("/login")
def login(data: LoginRequest):
    conn = get_db()
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