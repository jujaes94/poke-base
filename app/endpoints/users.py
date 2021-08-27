from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.schemas.users import UserCreate
from app.db.config import db_session, Session
from app.db.tables import Users_table, Pokemons_table
from app.utils.base import validate_email, validate_password, encrypt_password
from app.utils.security import decode_token, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, create_token
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/sign-up/", status_code=201)
async def sign_up(
    user_new: UserCreate,
    session: Session = Depends(db_session)
):

    """
    Service to sign up users
    """

    #validate password and email
    if not validate_email(user_new.email):
        raise HTTPException(
            status_code=400,
            detail="Please, enter a valid email."
        )
    
    if not validate_password(user_new.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password, please use a minimun of 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ]."
        )

    email = user_new.email.lower()

    #checks if the user already exists 
    user_db = session.query(Users_table).filter(Users_table.email == email).first()
    if user_db:
        print(f'User already exists id -> {user_db.id}')
        raise HTTPException(
            status_code=400,
            detail="The user already exists."
        )

    #hash password
    h_password = encrypt_password(user_new.password)

    print('Creating user')
    user_dict = user_new.dict()
    user_dict['password'] = h_password

    #adding and commiting new user
    new_user = Users_table(**user_dict)
    session.add(new_user)
    session.commit()

    print('User created')
    return "User created"


@router.post("/login/")
async def login(
    user_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(db_session)
):
    """
    Service for loging
    """

    #validate email
    if not validate_email(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Please, enter a valid email."
        )

    # checks if user exists
    user_db = session.query(Users_table.id, Users_table.email, Users_table.password).filter(Users_table.email == user_data.username.lower()).first()
    if not user_db:
        raise HTTPException(
            status_code=400,
            detail="User not found."
        )

    print(f'User found -> {user_db}')

    # validate password 
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password, please use a minimun of 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ]."
        )

    # checks if the email has the same password
    h_password = encrypt_password(user_data.password)
    if not h_password == user_db.password:
        raise HTTPException(
            status_code=400,
            detail='Invalid password or email'
        )

    # generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"user_id":user_db[0], "email": user_db[1]}, expires_delta=access_token_expires
    )

    print(f'Token generated -> {access_token}')

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.put("/favorite-pokemons/")
async def like_public_pokemon(
    id_pokemon: int,
    user: dict = Depends(decode_token),
    session: Session = Depends(db_session)
):
    """
    Service for update the user pokemon preferences 
    """
    try:
        print('Preparing for add favorite pokemon')
        # check for the pokemon
        pokemon = session.query(Pokemons_table).filter(Pokemons_table.id==id_pokemon).first()
        if not pokemon:
            raise ValueError('Pokemon not found')
        
        if pokemon.owner_id:
            raise ValueError('Pokemon its not public, choose another pokemon without owner')

        #update list of favorite pokemon
        print('Consulting user info')
        user_db = session.query(Users_table).filter(Users_table.id==user['user_id']).first()
        if not user_db:
            raise ValueError('User not found')

        print(f'User -> {user_db.__dict__}')
        if user_db.favorite_pokemons:
            
            if str(id_pokemon) in user_db.favorite_pokemons:
                raise ValueError('Pokemon already on the list')

            user_db.favorite_pokemons.append(id_pokemon)
        
        else:
            user_db.favorite_pokemons = [id_pokemon]
        
        print(f'User info to update -> {user_db.__dict__}')
        session.add(user_db)
        session.commit()

        return 'Pokend added to the list'

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