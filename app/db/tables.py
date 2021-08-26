from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from sqlalchemy.sql.expression import column

Base = declarative_base()

class User(Base):

    # se definino nombre de la tabla
    __tablename__ = 'users'

    # se define campos de la tabla como atributos
    id = Column(Integer(),primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())
    password = Column(String(),nullable=False)
    rol = Column(String())

    def __str__(self):
        return self.email

class Movies(Base):
    # se definino nombre de la tabla
    __tablename__ = 'movies'

    # se define campos de la tabla como atributos
    id = Column(Integer(),primary_key=True)
    name = Column(String(50), nullable=False)
    director = Column(String(50))
    created_at = Column(DateTime())

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