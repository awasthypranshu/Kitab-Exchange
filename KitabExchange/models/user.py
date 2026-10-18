#Models for users creeate,update
from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime

class User(SQLModel,table=True):
    id:Optional[int] = Field(index=True,primary_key=True)
    username:str = Field(index=True)
    email:str 
    college:str

    #one user can have many books
    books: List["Book"] = Relationship(back_populates="owner")

class CreateUser(SQLModel):
    username:str
    email:str 
    college:str

class UserRead(SQLModel):
    id:int
    username:str
    email:str 
    college:str
    

from model.books import Book
User.model_rebuild()
