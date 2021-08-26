from fastapi import APIRouter, Depends, HTTPException
from app.db.config import db_session, Session
from app.db.tables import Pokemons_table
from app.utils.security import decode_token
from app.schemas.pokemons import PokemonsBase, Pokemons


router = APIRouter()

@router.post("/")
async def add_pokemon(
    pokemon_new: PokemonsBase,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Service for create pokemon in DB
    """
    print('Preparing for create a pokemon')
    print(f'Pokemon input -> {pokemon_new}')
    
    try:
        poke_dict = pokemon_new.dict()

        poke_dict['owner_id'] = user.get('user_id')
        pokemon = Pokemons_table(**poke_dict)
        session.add(pokemon)
        session.commit()

        print('pokemon added successfully')
        return 'pokemon added successfully'
    except Exception as err:
        print(f'Error at create pokemon -> {err}')
        raise HTTPException(
            status_code=400,
            detail='Error at create pokemon'
        )

@router.post("/wild/")
async def add_wield_pokemons(
    pokemon_new: PokemonsBase,
    session: Session = Depends(db_session)
):
    """
    Service for add a wild pokemon in DB without an owner (public pokemons)
    """
    print('Preparing for create a pokemon')
    print(f'Pokemon input -> {pokemon_new}')
    
    try:

        pokemon = Pokemons_table(**pokemon_new.dict())
        session.add(pokemon)
        session.commit()

        print('pokemon added successfully')
        return 'pokemon added successfully'
    except Exception as err:
        print(f'Error at create pokemon -> {err}')
        raise HTTPException(
            status_code=400,
            detail='Error at create pokemon'
        )

