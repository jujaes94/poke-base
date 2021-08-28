from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.tables import Base, Users_table, Pokemons_table
from pydantic import Field
import os
import json

# session = None
# engie = None
# Session = None

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
Base.metadata.drop_all(engie)
Base.metadata.create_all(engie)

def db_init():
    print('loading data to db..')
    file = open('./app/db/data.json','r')
    data = json.load(file)

    for user in data['users']:
        # print('....',user)
        us = Users_table(**user)
        session.add(us)
    
    session.commit()

    for poke in data['pokemons']:
        pk = Pokemons_table(**poke)
        session.add(pk)

    session.commit()
    file.close()

async def db_session():
    return session
