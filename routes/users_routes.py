
from fastapi import APIRouter, HTTPException, status
from schemas.user_schemas import User
from db import user_db

from fastapi import Depends
from sqlalchemy.orm import Session
from db.connection import get_db
import time

user_router = APIRouter(tags=["User"])

@user_router.get("/test2")
async def test2(db : Session = Depends( get_db ) ) -> dict:
    print("db : ", db)
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/test")
async def test() -> dict:
    db = get_db()
    print("db : ", db)
    print("db next : ", next(db) )
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/")
async def get_users( db : Session = Depends(get_db) ) -> list[User] | None :
    users = await user_db.get_users( db )
    #print( users )
    if not users:
        raise HTTPException(
            status_code=404, detail="데이터가 없습니다"
            )
    return users

@user_router.get("/{email}",
                  response_model=User,
                  status_code=201
                  )
async def get_user(email : str) :
    print("email route 연결 : ", email)
    user = await user_db.get_user( email )
    print( user )
    if user:
        return user
    raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND , 
                    detail="존재하는 사용자 없음!"
                )

@user_router.post("/",
                  response_model=User,
                  status_code=201,
                  summary="회원가입입니다",
                  responses={ 409:{"description":"중복id"} }
                  )
async def post_user(user : User, db : Session = Depends(get_db) ) -> User:
    #print("사용자 추가 router : ", user)
    result = await user_db.insert( user, db )
    if not result: #None 거짓
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "중복된 id 입니다."
        )
    return result

@user_router.put("/{username}")
async def update_user( username:str , user:User):
    #print( "라우터 연결" )
    #print( username )
    #print( user )
    
    result = await user_db.update(username, user)
    if result:
        return result
    raise HTTPException(
                status_code=404, 
                detail="수정 사용자 id 없음!!!"
        )
    #return None

@user_router.delete("/{username}")
async def delete_user(username : str) -> User:
    result = await user_db.delete( username )
    if result:
        return result
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

