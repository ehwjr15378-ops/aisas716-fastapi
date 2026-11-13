import uvicorn
from fastapi import FastAPI
from routes.users_routes import user_router
from routes.auth_route import auth_router
from routes.file_route import file_router


from contextlib import asynccontextmanager

from models import user_model
from db.connection import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 서버 시작 시 설정 내용 ---")
    #print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    yield
    print("--- 서버 종료 시 설정 내용 ---")

app = FastAPI(lifespan=lifespan)

app.include_router( user_router , prefix="/users")
app.include_router( auth_router , prefix="/auth")
app.include_router( file_router , prefix="/files")

'''
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
'''


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
    #http://localhost:8000/docs