from fastapi import APIRouter, HTTPException, Depends, status
from packages import database, models, schemas
from sqlalchemy.orm import Session
from dependency import get_db
from hashing import password_hash, verify_hashed_password



router = APIRouter(

    tags=['Authenticatoion']
)

@router.post("/signup", response_model=schemas.UserCreate)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code= status.HTTP_208_ALREADY_REPORTED, detail="Email Already Exist try another")
    
    hashed_pw = password_hash(user.password)
    get_user = models.User(email = user.email, password = hashed_pw, is_active = True)

    db.add(get_user)
    db.commit()
    db.refresh(get_user)

    return get_user


@router.post("/login", response_model=schemas.UserLogin)
async def login(user : schemas.UserLogin, db:Session = Depends(get_db)):

    get_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not get_user : 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
    
    if not verify_hashed_password(user.password,get_user.password):
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Incorrect Password")
    
    return get_user
    


