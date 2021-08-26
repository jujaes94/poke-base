from pydantic import BaseModel
from typing import Optional

# clase base para usuarios
class UsersBase(BaseModel):
    email: str
    rol: Optional[str] = None

class User(UsersBase):
    id: int

# clase para crear usuario
class UserCreate(UsersBase):
    password: str
    newPassword: str