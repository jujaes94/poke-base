from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.sql.functions import user
from app.schemas import users
from app.db.config import db_session, Session
from app.db.tables import User
from app.utils.base import validate_email, validate_password, encrypt_password

router = APIRouter()

@router.get("/")
async def get_users():
    """
    Get all the users.
    """
    return 'ok'

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
    user_data: users.UserPass,
    session: Session = Depends(db_session)
):
    """
    Service for loging
    """

    #validate email
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Please, enter a valid email."
        )

    # checks if user exists
    user_db = session.query(User.id, User.email, User.password).filter(User.email == user_data.email.lower()).first()
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

    return 'ok'