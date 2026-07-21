from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ..database import get_session
from ..database_models import Post, Vote
from ..public_models import PublicPost, PublicUser, PublicVote
from ..security import get_current_user
from ..utilities import get_id_by_username, new_post

router = APIRouter(
    prefix="/votes",
    tags=["VOTES"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def like(user: Annotated[PublicUser, Depends(get_current_user)],
               vote: PublicVote,
               session=Depends(get_session)):
    
    voted_post = session.query(Vote).filter(Vote.id == vote.post_id, Vote.user_id == user.id).first()
    if voted_post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted for this post")
    elif vote.dir == 1:
        new_vote = Vote(user_id=user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added successfully"}
    
