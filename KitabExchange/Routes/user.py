from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlmodel import Session,select
from database import create_db_and_tables,get_session
from models.user import User,CreateUser,UserRead
from models.books import Book,BookCreate,BookUpdate
from auth import check_auth
app = FastAPI()

router = APIRouter(prefix="/user",tags=["User"])

@app.post("/register",response_model=UserRead)
async def register(user:CreateUser,session:Session=Depends(get_session)):
    #check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists")

    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
    
@app.get("/",response_model=list[User])
def list_users(session:Session=Depends(get_session)):
    """List all users"""
    users = session.exec(select(User)).all()
    return users