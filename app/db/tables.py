from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

from sqlalchemy.sql.expression import column

Base = declarative_base()

class Users_table(Base):

    # stablish table name
    __tablename__ = 'users'

    # stablish columns
    id = Column(Integer(),primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())
    password = Column(String(),nullable=False)
    favorite_pokemons = Column(ARRAY(String))
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False) 
    pokemon_trainer = Column(Boolean())
    phone = Column(Integer())

    def __str__(self):
        return self.email

class Pokemons_table(Base):
    # stablish table name
    __tablename__ = 'pokemons'

    # stablish columns
    id = Column(Integer(),primary_key=True)
    name = Column(String(50), nullable=False)
    nickname = Column(String(50)) 
    owner_id = Column(Integer())
    created_at = Column(DateTime(), default=datetime.now())
    atack = Column(Integer())
    defense = Column(Integer())
    spe_atack = Column(Integer())
    spe_defense = Column(Integer())
    next_evolution = Column(String(50))

    def __str__(self):
        return self.name


class Errors(Base):
    # se definino nombre de la tabla
    __tablename__ = 'errors'

    # se define campos de la tabla como atributos
    id = Column(Integer(),primary_key=True)
    code = Column(Integer(), nullable=False)
    detail = Column(String(50))

    def __str__(self):
        return self.code