from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from ..import models, schemas, hashing
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/user",
    tags= ['users']   
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}",status_code=200,response_model=schemas.ShowUser)
def get_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"item with id {blog_id} does not exists"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {user_id} does not exists")
    return user