from fastapi import FastAPI,Depends
from database import create_db_and_tables,get_session
from models.user import User,CreateUser,UserRead
from models.books import Book,BookCreate,BookUpdate
from auth import check_auth
from Routes import user,books
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Database connection established")

app.include_router(user.router)
app.include_router(books.router)

@app.get("/health")
def health_check():
    return {"message":"Welcome to KitabExchange API"}