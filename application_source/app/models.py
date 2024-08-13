from tokenize import String

from sqlalchemy import Column,Integer,String,ForeignKey,Date,Float
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    year_published = Column(Date)
    summary = Column(String)
    reviews = relationship('Reviews', back_populates='books')

class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    review_text = Column(String)
    rating = Column(Integer)
    book_id = Column(Integer, ForeignKey('books.id'))
    books = relationship('Books',back_populates='reviews')

