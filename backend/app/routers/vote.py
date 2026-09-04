from fastapi import (  # noqa: F401
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import engine, get_db

# -------------------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------------

router = APIRouter(prefix="/votes", tags=["Votes"])

# -------------------------------------------------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote,
                db: Session = Depends(get_db),  # noqa: B008
                current_user:int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==   
    vote.post_id,models.Vote.user_id == vote.user_id)

    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already vote on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = vote.user_id)
    
        db.add(new_vote)
        db.commit()

        return {"message" : "successfully added vote"}


    else:
        if not found_vote:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfully deleted vote"}