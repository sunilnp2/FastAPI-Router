from fastapi import APIRouter,HTTPException, Depends, status
from packages import database, models, schemas
from sqlalchemy.orm import Session
# from  import engine
from dependency import get_db

models.Base.metadata.create_all(bind=database.engine)





router = APIRouter(
    tags=["Sunil Blog"]
)

@router.get("/blog/")
async def get_all_blog(db:Session = Depends(get_db)):
    one_item = db.query(models.Blog).all()
    if one_item:
        return one_item
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@router.get("/blog/{blog_id}")
async def get_blog(blog_id :int, db:Session = Depends(get_db)):
    one_item = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if one_item:
        return one_item
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@router.post("/blog_create", response_model=schemas.BlogCreate)
async def create_blog(blog : schemas.BlogCreate, db: Session = Depends(get_db)):
    blog_item = models.Blog(**blog.dict())
    db.add(blog_item)
    db.commit()
    db.refresh(blog_item)
    return blog_item

@router.put("/update_blog/{blog_id}", response_model=schemas.BlogUpdate)
async def update_blog_id(blog_id : int, blog:schemas.BlogUpdate, db:Session = Depends(get_db)):

    # get_item = get_blog(db = db,blog_id = blog_id)
    get_item = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if get_item is not None:
        for key ,value in blog.dict(exclude_unset=True).items():
            setattr(get_item,key,value)
        db.commit()
        return get_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not Found")


@router.delete("/delete_blog/{blog_id}")
async def delete_blog(blog_id : int, db: Session = Depends(get_db)):

    get_item = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if get_item is not None:
        db.delete(get_item)
        db.commit()

        return get_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not Found")




    