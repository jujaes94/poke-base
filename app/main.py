from fastapi import FastAPI
from app.endpoints import pokemons, users

# se declara app como la aplicación de FastApi
app = FastAPI()

# se agregan los respectivos routers a app, indicando router, prefijo y tag
app.include_router(pokemons.router, prefix='/pokemons', tags=['pokemons'])
app.include_router(users.router, prefix="/users", tags=['users'])

@app.on_event('startup')
def db_init():
    from app.db.config import db_init
    db_init()