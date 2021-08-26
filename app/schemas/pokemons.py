from pydantic import BaseModel
from typing import Optional, Any

class PokemonsBase(BaseModel):
    name: str
    nickname: Optional[str]
    atack: Optional[int]
    defense: Optional[int]
    spe_atack: Optional[int]
    spe_defense: Optional[int]
    next_evolution: Optional[str]

class Pokemons(PokemonsBase):
    created_at: Any
    id: int
    owner_id: Optional[int]
