from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = ("mysql+pymysql://root:mysql@localhost:3306/fastapi")
engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker( autoflush=False, bind=engine )

def get_db():
    print("db 연결 시작")
    db = SessionLocal()
    try:
        yield db #"DB연결객체"
    finally:
        db.close()
        print("db 종료")