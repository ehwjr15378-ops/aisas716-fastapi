from fastapi import APIRouter, HTTPException, status

from schemas.auth_schemas import UserSignIn
from db.user_db import get_user

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/signin")
async def signin_user(data : UserSignIn) -> dict:
    #print("test")
    result = await get_user(data.email)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="회원 가입 먼저진행!!!")
    else:
        if data.password == result.password:
            return {"msg":"인증성공"}
        raise HTTPException(
                    status_code=403,
                    detail="비밀번호 틀림!!!")
    