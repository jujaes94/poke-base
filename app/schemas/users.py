from pydantic import BaseModel
from typing import Optional, Any, List

class UsersBase(BaseModel):
    email: str
    name: str
    last_name: str
    pokemon_trainer: bool = False
    phone: Optional[int]

class UserCreate(UsersBase):
    password: str

class User(UserCreate):
    id: int
    created_at: Any
    favorite_pokemons: List[str]