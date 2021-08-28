from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.tables import Base
from pydantic import Field
import os

print('Stablish connection with DB')
print('Getting engie...')
URL = os.getenv('DATABASE_URL')
# coneción al engie postgres
# engie = create_engine('postgresql://postgres:admin@localhost/movies')
engie = create_engine(URL)
# declaración de base

print('Getting session...')

# creación de la clase sesión
Session = sessionmaker(engie)
session = Session()

print('Setting db ...')
# Base.metadata.drop_all(engie)
Base.metadata.create_all(engie)

async def db_session():
    # reinicio de tablas, elimiando anteriores y creando nuevas
    return session
