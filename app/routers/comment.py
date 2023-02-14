from fastapi import status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from ..router import APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)

@router.post("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentFullResponse)
def create_comment(post_id: int, comment: schemas.CommentBase, 
                   db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.PostTable).filter(models.PostTable.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} was not found")            

    new_comment = models.CommentsTable(post_id = post.id, owner_id = current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
                   
    comment_query = db.query(models.CommentsTable).filter(models.CommentsTable.id == comment_id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id {comment_id} was not found")

    post_query = db.query(models.PostTable).filter(models.PostTable.id == comment.post_id)
    post = post_query.first()

    if comment.owner_id != current_user.id and post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to performe this action")

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)