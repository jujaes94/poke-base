from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# coneción al engie postgres
engie = create_engine('postgresql://postgres:admin@localhost/movies')

# declaración de base
Base = declarative_base()

class User(Base):

    # se definino nombre de la tabla
    __tablename__ = 'users'

    # se define campos de la tabla como atributos
    id = Column(Integer(),primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.username

# creación de la clase sesión
Session = sessionmaker(engie)
session = Session()

if __name__ == '__main__':
    Base.metadata.drop_all(engie)
    Base.metadata.create_all(engie)

    user1 = User(username='user1', email='algo@aloc.com')
    user2 = User(username='user2', email='algo2@aloc.com')
    user3 = User(username='user3', email='algo3@2aloc.com')

    session.add(user1)
    session.add(user2)
    session.add(user3)

    session.commit()