from schemas.user_schemas import User
from sqlalchemy.orm import Session
from models import user_model

users : list[User] = [
    User(username="aaa", password="aaa", email="aaa@aaa.aaa", name="홍길동"),
    User(username="bbb", password="bbb", email="bbb@bbb.bbb", name="김개똥"),
]

async def get_users( db : Session) -> list[User]:
    userTable = db.query(user_model.User).all()
    print("user table : ", userTable )
    if len(userTable) == 0: #not userTable
        return None
    #users = User( **userTable.model_dump() )
    users = [User.model_validate(user) for user in userTable]
    '''
    users = []
    for user in userTable: #userTable = [객체1, 객체2]
        users.append( User.model_validate(user) ) #db모델 -> 스키마 변환
    '''
    return users

async def get_user(email : str) -> User | None:
    print("email 데이터베이스 연결 : ",email)
    for u in users:
        print( u )
        if u.email == email:
            return u
    return None

async def insert( user : User , db : Session) -> User | None:
    exist_user =  ( 
                    db.query(user_model.User)
                    .filter( user_model.User.username == user.username )
                    .first()
                  )
    if exist_user:
        return None
    userTable = user_model.User( **user.model_dump() )
    print("저장 전 확인 id : ",userTable.id ) #id 없음
    db.add( userTable ) #insert db 임시 저장
    db.commit() #db 완벽히 저장
    db.refresh(userTable) #저장된 정보를 다시 가져옴
    print("저장 후 확인 id : ",userTable.id) #id 존재함

    return user
'''
users : list[User] = [
    User(username="aaa", password="aaa", email="aaa@aaa.aaa", name="홍길동"),
    User(username="bbb", password="bbb", email="bbb@bbb.bbb", name="김개똥"),
]
'''
async def update( username:str, user:User):
    for i, u in enumerate(users):
        if u.username == username:
            users[i] = user
            #u = user
            return u
    return None

async def delete( username:str ):
    for i, u in enumerate(users):
        if u.username == username:
            del_user = users.pop( i )
            return del_user
    return None
    