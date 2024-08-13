from sqlalchemy import select

from app.database import get_session
from fastapi import status,APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.routers.login import get_current_user
from passlib.context import CryptContext

pwd_content = CryptContext(schemes=['bcrypt'], deprecated="auto")

router = APIRouter(tags=['User'])

@router.get("/user")
async def get_user(db: AsyncSession = Depends(get_session),current_user:schemas.User=Depends(get_current_user)):
    user = await db.execute(select(models.User))
    return user.scalars().all()


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.User,db: AsyncSession = Depends(get_session)):
    hashed_password=pwd_content.hash(request.password)
    result = await db.execute(select(models.User).filter(models.User.username == request.username))
    existing_user =result.scalar_one_or_none()
    if existing_user is None:
        user = models.User(username=request.username, email=request.email, password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    else:
        raise HTTPException(detail="Username already exist",status_code=status.HTTP_400_BAD_REQUEST)