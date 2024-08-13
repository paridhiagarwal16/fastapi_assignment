from urllib.request import Request
from sqlalchemy import select
from fastapi import APIRouter
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

SECRET_KEY = 'b8b4bbb762c5f9148bb9f373b0abecda41c983cad64f1b53a153780436dccf33'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

ouath2_scheme = OAuth2PasswordBearer(tokenUrl='login')
pwd_content = CryptContext(schemes=['bcrypt'], deprecated="auto")
router = APIRouter(tags=['Authentication'])


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await db.execute(select(models.User).filter(request.username == models.User.username))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pwd_content.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    access_token = generate_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(ouath2_scheme)):
    crendential_exception = HTTPException(
        detail="Invalid auth credentials",
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={'www-authenticate': "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise crendential_exception
        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError as e:
        raise crendential_exception
