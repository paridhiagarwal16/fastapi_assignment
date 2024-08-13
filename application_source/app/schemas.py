from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import date
class Review(BaseModel):
    user_id : int= Field(examples=[1])
    review_text : str= Field(examples=["A very nice book"])
    rating : int= Field(examples=[4])

    class Config:
        from_attributes = True



class Books(BaseModel):
    title  :str=Field(examples=["Harry Potter"])
    author : str= Field(examples=["JK Rowling"])
    genre : str= Field(examples=["Thrill"])
    year_published : date= Field(examples=["2024-01-01"])
    summary : str= Field(examples=["Harry Potter discovers the magical world."])


    class Config:
        from_attributes = True



class User(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : Optional[str] = None