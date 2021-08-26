from fastapi import APIRouter
from app.db.config import db_session, Session


router = APIRouter()

@router.get("/")
async def get_movies():
    return 'hello world'
