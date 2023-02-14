from fastapi import Response, status, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text, func

from ..router import APIRouter
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostFullResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                                                                    limit: int = 10, search: Optional[str] = ""):

    posts_query = db.query(models.PostTable, func.count(models.CommentsTable.post_id).label("comments")).join(
        models.CommentsTable, models.CommentsTable.post_id == models.PostTable.id, isouter=True).group_by(
            models.PostTable.id).filter(models.PostTable.title.contains(search)).limit(limit)

    posts_list = [{"id": post[0].id,
                   "title": post[0].title,
                   "content": post[0].content,
                   "published": post[0].published,
                   "created_at": post[0].created_at,
                   "owner": post[0].owner,
                   "comments": post[1]} for post in posts_query]


    return posts_list


@router.get("/{id}", response_model=schemas.PostFullResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.PostTable, func.count(models.CommentsTable.post_id).label("comments")).join(
        models.CommentsTable, models.CommentsTable.post_id == models.PostTable.id, isouter=True).group_by(
            models.PostTable.id).filter(models.PostTable.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    post_dict = {"id": post[0].id,
                 "title": post[0].title,
                 "content": post[0].content,
                 "published": post[0].published,
                 "created_at": post[0].created_at,
                 "owner": post[0].owner,
                 "comments": post[1]}

    return post_dict


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateResponse)
def create_post(post: schemas.PostBase, 
                db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.PostTable(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.PostTable).filter(models.PostTable.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to performe this action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostCreateResponse)
def update_post(id: int, post_new_data: schemas.PostUpdateBase, 
                db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
                
    post_query = db.query(models.PostTable).filter(models.PostTable.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to performe this action")

    post_query.update(post_new_data.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.get("/{id}/comments", response_model=List[schemas.CommentFullResponse])
def get_post_comments(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.PostTable).filter(models.PostTable.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    comments = db.query(models.CommentsTable).filter(models.CommentsTable.post_id == post.id).all()

    return comments
