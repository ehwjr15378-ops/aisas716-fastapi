
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db.connection import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username : Mapped[str] = mapped_column( String(100), unique=True)
    password : Mapped[str] = mapped_column( String(100))
    email : Mapped[str] = mapped_column( String(100), unique=True)
    name : Mapped[str] = mapped_column( String(100) )


