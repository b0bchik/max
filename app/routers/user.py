from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_session
from ..public_models import PublicUser
from ..security import authenticate_user, create_access_token
from ..utilities import new_user

router = APIRouter(
    prefix="/users",
    tags=["USER"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED,)
async def create_user(user: PublicUser, session=Depends(get_session)):
    new_user(session, user.username, user.email, user.password)
    return {"message": "User created successfully"}

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
