
import datetime
from jose import JWTError, jwt, ExpiredSignatureError
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from datetime import timedelta, datetime

SECRET_KEY = 'ee2650af9cd95bdb72a2aff7342c9b6cce2299bc0187ecf37510f0ac79e60f00'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

class token(BaseModel):
    token: str
    token_type: str

#declaration of auth_schema who handle password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/")

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    print('creating token')
    to_encode = data.copy()
    if expires_delta:
        print(f'expire -> {expires_delta}')
        expire = datetime.utcnow() + expires_delta
    else:
        print('Expire default')
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print('Token encoded')

    return encoded_jwt

def decode_token(token: str = Depends(oauth2_scheme)):
    print(f'getting data from token -> {token}')
    #responde error
    credentials_exception = HTTPException(
        status_code=401,
        detail='Error at validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'Token encoded -> {payload}')
        if payload is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=400,
            detail='Signature has expired'
        )
    except JWTError:
        raise credentials_exception
    
    return {'user_id': payload.get('user_id'), 'email': payload.get('email')}