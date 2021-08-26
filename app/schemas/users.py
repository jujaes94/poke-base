from pydantic import BaseModel
from typing import Optional

class UsersBase(BaseModel):
    email: str
    rol: Optional[str] = 'client'

class User(UsersBase):
    id: int

class UserPass(UsersBase):
    password: str