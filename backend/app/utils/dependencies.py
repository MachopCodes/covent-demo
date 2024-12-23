from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import DBUser
from app.utils.jwt import SECRET_KEY, ALGORITHM

def get_current_user(db: Session = Depends(get_db), token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
