# from fastapi import Response,status,HTTPException,Depends,APIRouter
# from fastapi.params import Body
# from typing import Optional
# from  .. import models
# from .. import schemas
# # from .schemas import Post,PostCreate,UserCreate,UserOut
# from  ..database import engine,sessionmaker,SessionLocal,get_db
# from sqlalchemy.orm import Session
# from typing import List

#router=APIRouter()


from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router=APIRouter(prefix='/posts',tags=['posts'])
import oauth2






@router.get('/',response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts





# @router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def create_post(new_post:schemas.PostCreate,db:Session=Depends(get_db)):
#     #updated_post:schemas.PostCreate  
#     new_post=models.Post(**new_post.model_dump())
#     print(new_post)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return [new_post]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post_model = models.Post(**new_post.dict())  # Use dict() instead of model_dump()
    db.add(new_post_model)
    db.commit()
    db.refresh(new_post_model)
    return new_post_model # Return a list of the created post





@router.get('/{id}',response_model=schemas.Post)
def get_posts(id:int,db:Session=Depends(get_db)):     
    #post=find_post(id)  #type str
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} not found')
       
    return {'post_details':post}



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {id} not available')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put('/{id}',response_model=schemas.Post)
def update_posts(id:int,updated_post:schemas.PostCreate   ,db: Session = Depends(get_db)):

    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id:{id} not found")
    

    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    
    
    return post_query.first()


