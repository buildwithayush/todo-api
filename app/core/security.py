from pwdlib import PasswordHash
import jwt
from datetime import datetime,timedelta,timezone


SECRET_KEY = 'SUPER_SECRET_KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

def hash_password(plain_password:str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str , hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict) -> str:
    to_encode= data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt