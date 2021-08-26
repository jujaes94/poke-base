
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

#declaration of auth_schema who handle password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/")

def decode_token(token: str):
    print(f'decoding token {token}')
    return {'email': 'algo'}

def get_data(token: str = Depends(oauth2_scheme)):
    print('Getting data')
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Session has expired.",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    return user

def get_active_data(current_user: dict = Depends(get_data)):
    print('Validating time session ')
    return current_user