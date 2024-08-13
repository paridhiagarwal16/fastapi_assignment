from sqlalchemy.future import select

from app.database import get_session
from fastapi import status,APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app import models, schemas
from app.routers.login import get_current_user
from passlib.context import CryptContext

pwd_content = CryptContext(schemes=['bcrypt'], deprecated="auto")

router = APIRouter(tags=['Reviews'])

@router.get("/books/{id}/reviews")
async def get_reviews(book_id:int,db: AsyncSession = Depends(get_session),
                      current_user:schemas.User=Depends(get_current_user)):

    print("inside func get_reviews")
    result = await db.execute(select(models.Books).filter(models.Books.id == book_id))
    print("filter result")
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Reviews not found")
    reviews = await db.execute(select(models.Reviews).filter(models.Reviews.book_id == book.id))
    return reviews.scalars().all()



@router.post("/books/{id}/reviews", status_code=status.HTTP_201_CREATED)
async def create_review(book_id:int,request: schemas.Review,db: AsyncSession = Depends(get_session),
                        current_user:schemas.User=Depends(get_current_user)):

    print("bookid",book_id)
    result=await db.execute(select(models.Books).filter(models.Books.id == book_id))
    book=result.scalar_one_or_none()
    print("book ",book)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Book not found')

    review = models.Reviews(user_id=request.user_id, review_text=request.review_text,
                           rating=request.rating,book_id=book_id)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

