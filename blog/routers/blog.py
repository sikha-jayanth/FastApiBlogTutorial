from fastapi import APIRouter
from fastapi import Depends, status,Response,HTTPException
from sqlalchemy.sql.functions import user
from ..import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from blog.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/blog",
    tags= ['blogs']   
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title,body=blog.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#view all blogs with authorized access
@router.get("/", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{blog_id}",status_code=200,response_model=schemas.ShowBlog)
def get_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"item with id {blog_id} does not exists"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item with id {blog_id} does not exists")
    return blog

@router.delete("/{blog_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==blog_id).delete(synchronize_session=False)
    db.commit()
    return "done"

@router.put("/{blog_id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, blog: schemas.Blog,db: Session = Depends(get_db)):
    # db.query(models.Blog).filter(models.Blog.id==blog_id).update(blog.dict())
    blog_update = db.query(models.Blog).filter(models.Blog.id==blog_id)
    if not blog_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"item with id {blog_id} does not exists")
    blog_update.update(blog.dict())
    db.commit()
    return "updated successfully"