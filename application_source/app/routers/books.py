from app.database import get_session
from fastapi import status,APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.login import get_current_user
from typing import List
from sqlalchemy.future import select
from app import models, schemas


router = APIRouter(tags=['Books'])





@router.post("/books", status_code=status.HTTP_201_CREATED)
async def add(request: schemas.Books, db: AsyncSession = Depends(get_session),current_user:schemas.User=Depends(get_current_user)):
    new_book = models.Books(title=request.title,author=request.author,genre=request.genre,
                            year_published=request.year_published,
                            summary=request.summary)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return request


@router.get('/books')
async def get_books(db: AsyncSession = Depends(get_session),current_user:schemas.User=Depends(get_current_user)):
    result = await db.execute(select(models.Books))
    return result.scalars().all()

@router.get('/books/{id}')
async def get_book(book_id:int, db: AsyncSession = Depends(get_session),current_user:schemas.User=Depends(get_current_user)):
    try:
        query = select(models.Books).filter(models.Books.id == book_id)
        result = await db.execute(query)
        books = result.scalar_one_or_none()
        print(books)

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        return books
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.delete('/books/{id}')
async def delete_book(book_id:int, db: AsyncSession = Depends(get_session) , current_user:schemas.User=Depends(get_current_user)):
    try:
        result = await db.execute(select(models.Books).filter(models.Books.id == book_id))
        books = result.scalar_one_or_none()
        print("book found")
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        await db.delete(books)
        await db.commit()
        return {"message": "Book deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.put('/books/{id}')
async def update_book(book_id:int, request: schemas.Books, db: AsyncSession = Depends(get_session),current_user:schemas.User=Depends(get_current_user)):
    try:
        result = await db.execute(select(models.Books).filter(models.Books.id == book_id))
        existing_book = result.scalar_one_or_none()
        if not existing_book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        for key, value in request.dict().items():
            setattr(existing_book, key, value)


        db.add(existing_book)
        await db.commit()
        await db.refresh(existing_book)
        return existing_book

        await db.commit()
        return "Book updated"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
