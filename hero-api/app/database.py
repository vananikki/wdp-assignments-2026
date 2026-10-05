import os
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

# Lấy DATABASE_URL từ biến môi trường, nếu không có thì mặc định dùng sqlite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Nếu dùng SQLite cần thêm connect_args, còn PostgreSQL thì không bắt buộc
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# Tạo engine với echo=True để in ra các câu lệnh SQL ở terminal
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]