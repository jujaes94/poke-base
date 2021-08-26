from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.functions import user
from typing import Any
from app.schemas import users
from app.db.config import db_session, Session
from app.db.tables import User
from app.utils.base import validate_email, validate_password, encrypt_password
from app.utils.security import get_active_data, get_data, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, create_token
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
async def get_users(
    user: Any = Depends(get_active_data)
):
    """
    Get all the users.
    """
    return user

@router.post("/sign-up/", status_code=201)
async def sign_up(
    user_new: users.UserPass,
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
    user_db = session.query(User).filter(User.email == email).first()
    if user_db:
        print(f'User already exists id -> {user_db.id}')
        raise HTTPException(
            status_code=400,
            detail="The user already exists."
        )

    h_password = encrypt_password(user_new.password)

    print('Creating user')
    new_user = User(email=email, password=h_password, rol=user_new.rol)
    session.add(new_user)
    session.commit()

    print('User created')
    return "User created"


@router.post("/login/")
async def login(
    user_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(db_session),
    # token: str = Depends(oauth2_scheme)
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
    user_db = session.query(User.id, User.email, User.password).filter(User.email == user_data.username.lower()).first()
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
        data={"userid":user_db[0], "username": user_db[1]}, expires_delta=access_token_expires
    )

    return {'token': access_token, 'token_type': 'bearer'}