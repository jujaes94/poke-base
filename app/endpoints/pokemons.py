from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Union
from sqlalchemy.sql.expression import or_
from app.db.config import db_session, Session
from app.db.tables import Pokemons_table
from app.utils.security import decode_token
from app.schemas.pokemons import PokemonsBase, PokemonsEdit, PokemonsConsult


router = APIRouter()

@router.post("/")
async def add_pokemon(
    pokemon_list: List[PokemonsBase],
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Service for create one or multi pokemons in DB
    """
    print('Preparing for create a pokemon')
    
    try:
        for pokemon_new in pokemon_list:
            poke_dict = pokemon_new.dict()

            poke_dict['owner_id'] = user.get('user_id')
            pokemon = Pokemons_table(**poke_dict)
            session.add(pokemon)
            
        session.commit()

        print('pokemon added successfully')
        return f'total pokemon added {len(pokemon_list)}'
    except Exception as err:
        print(f'Error at create pokemon -> {err}')
        raise HTTPException(
            status_code=400,
            detail='Error at create pokemon'
        )

@router.post("/wild/")
async def add_wield_pokemons(
    pokemon_list: List[PokemonsBase],
    session: Session = Depends(db_session)
):
    """
    Service for add a wild pokemon in DB without an owner (public pokemons)
    """
    print('Preparing for create a pokemon')
    
    try:
        for pokemon_new in pokemon_list:
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
    page: int = 0,
    limit: int = 5,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Get pokemons who have an owner, are public or all from the table
    """
    try:
        
        if type.lower() == 'o':
            print(f'Getting only the pokemons who belong to {user["email"]}')

            pokemons = (
                session.query(Pokemons_table)
                .filter(Pokemons_table.owner_id == user['user_id'])
                .limit(limit).offset(page)
                .all()
            )

            print(f'Result query -> {pokemons}')
            if not pokemons:
                raise HTTPException(
                    status_code=400,
                    detail='No pokemons found.'
                )
        elif type.lower() == 'p':
            print(f'Getting only the public pokemons')

            pokemons = (
                session.query(Pokemons_table)
                .filter(Pokemons_table.owner_id == None)
                .limit(limit).offset(page)
                .all()
            )

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
                .limit(limit).offset(page)
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
                
        return [poke.__dict__ for poke in pokemons]

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
    
    
@router.put("/")
async def edit_pokemon(
    id_pokemon: int,
    pokemon_info: PokemonsEdit,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Edit pokemon by id if its the owner
    """
    try:
        print('Preparing for edit pokemon')
        #checks if the user is owner of the pokemon
        pokemon= session.query(Pokemons_table).filter(Pokemons_table.id==id_pokemon).first()
        if not pokemon:
            raise ValueError('Pokemon not found')
        elif not pokemon.owner_id == user['user_id']:
            raise ValueError('User its not the owner of the pokemon')

        #convert pokemon data input into dict
        print('Converting pokemon data into dict')
        poke_dict = pokemon_info.dict(exclude_unset=True)
        for key, value in poke_dict.items():
            print(f'Updating {key}')
            setattr(pokemon, key, value)

        session.add(pokemon)
        session.commit()

        return f'Pokemon {pokemon.name} updated'

        
    except ValueError as err:
        print(err,dir(err))
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

    except Exception as e:
        print(f'Error at edit pokemon -> {e}')
        raise HTTPException(
            status_code=400,
            detail='Error at edit pokemon'
        )


@router.delete("/")
async def delete_pokemons(
    id_pokemon: Optional[int] = None,
    all_pokemon: Optional[bool] = None,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Delete one owned pokemon or all of them
    """
    print(f'Preparing for delete pokemon {id_pokemon}')
    try:
        pokemon = []
        if id_pokemon and all_pokemon:
            raise ValueError('please, choose only one option for delete pokemon')

        elif id_pokemon:
            print('Searching for pokemon id')
            poke_query= session.query(Pokemons_table).filter(Pokemons_table.id==id_pokemon)
            pokemon = poke_query.first()
            if not pokemon:
                raise ValueError('Pokemon not found')
            elif not pokemon.owner_id == user['user_id']:
                raise ValueError('User its not the owner of the pokemon')

        elif all_pokemon:
            print('Searching for all pokemons owned')
            poke_query= session.query(Pokemons_table).filter(Pokemons_table.owner_id==user['user_id'])
            pokemon = poke_query.all()
            if not pokemon:
                raise ValueError('Pokemon not found')

        else:
            raise ValueError('Wrong option for id pokemon, please put a valid numeric number for id or type all for delete')

        print('Deleting pokemon')
        poke_query.delete()
        session.commit()

        return f'Pokemon {pokemon.name} - id {pokemon.id}, deleted' if id_pokemon else f'Total pokemons deleted {len(pokemon)}'

    except ValueError as err:
        print(err,dir(err),type(err))
        raise HTTPException(
            status_code=400,
            detail=str(err)
        )

    except Exception as e:
        print(f'Error at delete pokemon -> {e}')
        raise HTTPException(
            status_code=400,
            detail='Error at edit pokemon'
        )
