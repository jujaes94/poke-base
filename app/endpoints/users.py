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
    user_new: users.UserCreate,
    session: Session = Depends(db_session)
):

    """
    Service to sign up users
    """
    print(f'User data to register -> {user_new}')

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