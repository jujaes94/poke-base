from fastapi import FastAPI
from app.endpoints import movies

# se declara app como la aplicación de FastApi
app = FastAPI()

# se agregan los respectivos routers a app, indicando router, prefijo y tag
app.include_router(movies.router, prefix='/movies', tags=['movies'])
