from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

# Modular Imports
from app.database import get_db
from app.schemas.vote import Votes_PyModel
from app.schemas.user import User_PyModel
from app.utils import oauth2
from app.models.vote import Votes
from app.models.post import Posts


# Set route prefix
router = APIRouter(
    prefix="/v1/api/vote",
    tags=["Votes"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(pvote: Votes_PyModel, db: Session = Depends(get_db), current_user: User_PyModel = Depends(oauth2.get_current_user)):
    # print(f"SERVER: Vote for postID:[{pvote.post_id}] received from user:[{current_user.id}]")

    # query for checking if post exists or not
    found_post = db.query(Posts).filter(Posts.id == pvote.post_id).first()
    if not found_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post:{pvote.post_id} does not exist"
        )

    # query for vote of user for post
    vote_query = db.query(Votes).filter(Votes.post_id == pvote.post_id, Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    # according to vote direction
    if pvote.dir == 1:

        # user has already up voted post
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already up voted post:{pvote.post_id}"
            )

        # make new vote to Votes table
        new_vote = Votes(post_id=pvote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            "msg": "Successfully added vote"
        }

    else:
        # to remove a vote , there should be a vote by user on post
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote of user[{current_user.id}] for post:{pvote.post_id} could not be found"
            )

        # remove the entry from Votes table
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {
            "msg": "Successfully removed vote"
        }
