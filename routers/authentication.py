from fastapi import APIRouter, HTTPException, Depends, status
from packages import database, models, schemas
from sqlalchemy.orm import Session
from dependency import get_db
from hashing import password_hash, verify_hashed_password



router = APIRouter(

    tags=['Authenticatoion']
)

# code for get user using email
@router.get("/get_user/{user_id}")
def get_user(user_id:int, db:Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with This id not found")
    
    return get_user


# --------------------------code for signup-------------------------- 

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

#c--------------------------code for login --------------------------
@router.post("/login", response_model=schemas.UserLogin)
async def login(user : schemas.UserLogin, db:Session = Depends(get_db)):

    get_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not get_user : 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
    
    if not verify_hashed_password(user.password,get_user.password):
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Incorrect Password")
    
    return get_user


# code for update user info 
@router.put("/update_user/{user_id}", response_model=schemas.UserUpdate)
async def update_user(user_id:int, update_data : schemas.UserUpdate, db:Session = Depends(get_db)):

    my_user = get_user(db = db, user_id=user_id)

    # hashed_password = hashed_password(update_data.password)
    
    if my_user:
        for key, value in update_data.dict(exclude_unset=True).items():
            if key == "password":
                # Hash the new password before updating
                hashed_password = password_hash(update_data.password)
                setattr(my_user, key, hashed_password)
            else:
                setattr(my_user, key, value)

        db.commit()

    return my_user



# code for deleting user 

@router.delete("/delete_user/{user_id}")
async def delet_user(user_id:int, db:Session = Depends(get_db)):
    my_user = get_user(db = db, user_id=user_id)

    if my_user:
        db.delete(my_user)
        db.commit()
        
    return my_user


