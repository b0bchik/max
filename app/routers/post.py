from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import func

from ..database import get_session
from ..database_models import Post, Vote
from ..public_models import PublicPost, PublicUser
from ..security import get_current_user
from ..utilities import get_id_by_username, new_post


router = APIRouter(
    prefix="/post",
    tags=["POSTS"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PublicPost,
    current_user: Annotated[PublicUser, Depends(get_current_user)],
    session=Depends(get_session),
):
    new_post(session, post.title, post.content, current_user.id)
    return {"message": "Post created successfully"}


@router.get("/test")
async def test(
    session=Depends(get_session),
):
    res = session.query(Post, func.count(Vote.post_id).label("votes")).join(
        Vote, Vote.post_id == Post.id, isouter=True).group_by(Post.id).all()
    return {"res": res}


@router.get("/{post_id}", response_model=PublicPost)
async def get_post_by_id(
    post_id: Annotated[int, Path()],
    session=Depends(get_session),
):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "owner": {
            "username": post.owner.username,
            "email": post.owner.email,
            "password": post.owner.password,
        },
    }


@router.patch("/{post_id}")
async def update_post(
    post_id: Annotated[int, Path()],
    post: PublicPost,
    current_user: Annotated[PublicUser, Depends(get_current_user)],
    session=Depends(get_session),
):
    existing_post = session.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if existing_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    existing_post.title = post.title
    existing_post.content = post.content
    session.commit()
    return {"message": "Post updated successfully"}


@router.get("/user/{username}")
async def get_posts(
    current_user: Annotated[PublicUser, Depends(get_current_user)],
    username: Annotated[str, Path()],
    session=Depends(get_session),
):
    users_id = get_id_by_username(session, username)
    posts = session.query(Post).filter(Post.user_id == users_id).all()
    return {"posts": posts}


@router.delete("/delete_post/{post_id}")
async def delete_post(
    post_id: Annotated[int, Path()],
    current_user: Annotated[PublicUser, Depends(get_current_user)],
    session=Depends(get_session),
):
    existing_post = session.query(Post).filter(Post.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if existing_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    session.delete(existing_post)
    session.commit()
    return {"message": "Post deleted successfully"}