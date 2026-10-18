from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlmodel import Session,select
from database import create_db_and_tables,get_session
from typing import Optional
from models.user import User,CreateUser,UserRead
from models.books import Book,BookCreate,BookUpdate
from auth import check_auth
app = FastAPI()

routes = APIRouter(prefix="/book",tags=["Book"])

@routes.get("/",response_model=list[Book])
def list_books(author:Optional[str]=None,title:Optional[str]=None,session:Session=Depends(get_session)):
    """List all books"""
    if author and title:
        books = session.exec(select(Book).where(Book.author == author,Book.title == title)).all()
    elif author:
        books = session.exec(select(Book).where(Book.author == author)).all()
    elif title:
        books = session.exec(select(Book).where(Book.title == title)).all()
    else:
        books = session.exec(select(Book)).all()
    return books

@app.post("/bookCreate")
def book_create(book:BookCreate,api_key:str = Depends(check_auth),session:Session=Depends(get_session)):
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@app.patch("/updateBook/{book_id}",response_model=BookUpdate)
def book_update(book_id:int,book:BookUpdate,api_key:str = Depends(check_auth),session:Session=Depends(get_session)):
    existing_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not existing_book:
        raise HTTPException(status_code=404,detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    for key,value in book_data.items():
        setattr(existing_book,key,value)
        
    session.add(existing_book)
    session.commit()
    session.refresh(existing_book)
    return existing_book

@app.patch("/{book_id}/sold",response_model=BookUpdate)
def book_sold(book_id:int,api_key:str = Depends(check_auth),session:Session=Depends(get_session)):
    existing_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not existing_book:
        raise HTTPException(status_code=404,detail="Book not found")
    existing_book.is_sold = True
    session.add(existing_book)
    session.commit()
    session.refresh(existing_book)
    return existing_book