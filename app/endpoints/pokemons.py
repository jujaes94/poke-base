from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.sql.coercions import RoleImpl

from sqlalchemy.sql.expression import or_
from app.db.config import db_session, Session
from app.db.tables import Pokemons_table
from app.utils.security import decode_token
from app.schemas.pokemons import PokemonsBase, Pokemons, PokemonsConsult


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


@router.get("/", response_model=List[PokemonsConsult])
async def get_pokemons(
    type: str,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Get pokemons who have an owner, are public or all from the table
    """
    try:
        result = []
        if type.lower() == 'o':
            print(f'Getting only the pokemons who belong to {user["email"]}')

            pokemons = session.query(Pokemons_table).filter(Pokemons_table.owner_id == user['user_id']).all()
            print(f'Result query -> {pokemons}')
            if not pokemons:
                raise HTTPException(
                    status_code=400,
                    detail='No pokemons found.'
                )
        elif type.lower() == 'p':
            print(f'Getting only the public pokemons')

            pokemons = session.query(Pokemons_table).filter(Pokemons_table.owner_id == None).all()
            print(f'Result query -> {pokemons}')
            if not pokemons:
                raise HTTPException(
                    status_code=400,
                    detail='No pokemons found.'
                )

        elif type.lower() == 'a':
            print(f'Getting all the public pokemons and who belong to {user["email"]}')

            pokemons = (
                session.query(Pokemons_table)
                .filter(or_(Pokemons_table.owner_id == None, Pokemons_table.owner_id == user['user_id']))
                .all()
            )

            print(f'Result query -> {pokemons}')
            if not pokemons:
                raise HTTPException(
                    status_code=400,
                    detail='No pokemons found.'
                )
        else:
            raise ValueError('Wrong option')

        for poke in pokemons:
                print(f'Poke -> {poke}')
                result.append(poke.__dict__)
                
        return result

    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid option of type consult. Choose only 'a' (all), 'p' (public), or 'o' (owner)"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail='Error at get pokemons'
        )
    
    

