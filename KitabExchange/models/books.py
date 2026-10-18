from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime

class Book(SQLModel,table=True):
    id:Optional[int] = Field(index=True,primary_key=True)
    title:str
    author:str
    price:float
    is_sold:bool = Field(default=False)
    user_id:Optional[int] = Field(default=None,index=True,foreign_key="user.id")

    owner: "User" = Relationship(back_populates="books")

#request for creating a book 
class BookCreate(SQLModel):
    title:str
    author:str
    price:float
    user_id:Optional[int] = Field(default=None,index=True,foreign_key="user.id")

#request for updating a book 
class BookUpdate(SQLModel):
    price:Optional[float] = None
    is_sold:Optional[bool] = None

from model.User import User
Book.model_rebuild()    