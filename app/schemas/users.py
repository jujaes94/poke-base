from pydantic import BaseModel
from typing import Optional, Any

class UsersBase(BaseModel):
    email: str
    rol: Optional[str] = 'client'

class User(UsersBase):
    id: int
    created_at: Any

class UserPass(UsersBase):
    password: str