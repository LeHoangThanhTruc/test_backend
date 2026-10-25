#Là nơi liên kết những file khác (file chức năng, file d4ữ liệu5)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import auth

app = FastAPI()

# Bật CORS cho phép Android kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tự động tạo bảng nếu chưa có
init_db()

# Nhúng Router Auth vào ứng dụng
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Backend API đang chạy bình thường"}