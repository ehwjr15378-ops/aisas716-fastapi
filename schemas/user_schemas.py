from pydantic import BaseModel, EmailStr, ConfigDict

class User(BaseModel):
    username : str
    password : str
    email : EmailStr
    name : str

    model_config = ConfigDict(from_attributes=True)
