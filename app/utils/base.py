import re
import hashlib

def validate_email(email: str):
    """
    Validate sintax for an email string
    """
    
    print('checking email')
    regex = r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return True if re.fullmatch(regex, email) else False

def validate_password(password: str):
    """
    Check password from a regex that fullfil the next criteria:
    - At least one upppercase letter
    - At least one lowercase letter
    - At least 10 characters
    - One of the following characters: !, @, #, ? or ].
    """

    print('checking password')
    regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@!#?\]])[A-Za-z\d@!#?\]]{10,}$'
    return True if re.fullmatch(regex, password) else False

def encrypt_password(password: str):
    """
    Return an encrypted password with sha256 in a form of hexadecimal string
    """
    print('Encrypting password')
    return hashlib.sha256(password.encode()).hexdigest()

