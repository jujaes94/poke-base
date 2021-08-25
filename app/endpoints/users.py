from fastapi import APIRouter, HTTPException
from app.schemas import users

router = APIRouter()

@router.post("/sign-up/", status_code=201)
async def sign_up(
    user_in: users.UserCreate 
):

    """
    Service to sign up users into movies DB
    """
    #checks if the user already exists 
    user = True
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user already exists."
        )
    

    return "ok"