from fastapi import APIRouter, HTTPException, Depends
from app.schemas import users
from app.db.config import db_session, Session
from app.db.tables import User

router = APIRouter()

@router.get("/")
async def get_users():
    """
    Get all the users.
    """
    return 'ok'

@router.post("/sign-up/", status_code=201)
async def sign_up(
    user: users.UserCreate,
    session: Session = Depends(db_session)
):

    """
    Service to sign up users into movies DB
    """
    print(f'User data to register -> {user}')
    new_user = User(email=user.email, password=user.password)
    session.add(new_user)
    session.commit()

    print('User created')

    #checks if the user already exists 
    # user = True
    # if user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="The user already exists."
    #     )
    

    return "ok"