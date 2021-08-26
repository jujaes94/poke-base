from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from app.db.tables import Base

print('Stablish connection with DB')
print('Getting engie...')
# coneción al engie postgres
engie = create_engine('postgresql://postgres:admin@localhost/movies')
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
