from pydantic import BaseModel
from typing import Optional

# clase base para usuarios
class UsersBase(BaseModel):
    username: str
    id: int 

# clase para crear usuario
class UserCreate(UsersBase):
    password: str
    newPassword: str