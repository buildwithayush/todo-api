import jwt
from fastapi import status,HTTPException,Depends
from app.core.security import SECRET_KEY,ALGORITHM
from fastapi.security import HTTPBearer ,HTTPAuthorizationCredentials
from app.models.user_db import UserDB
from app.database import get_db
from sqlalchemy.orm import Session

security_scheme = HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security_scheme) , db:Session= Depends(get_db)) -> UserDB:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception


    user = db.query(UserDB).filter(UserDB.id == int(user_id)).first()

    if not user:
        raise credentials_exception

    return user