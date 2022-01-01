from fastapi import APIRouter, status, Depends
from profiles import db
from sqlalchemy.orm import Session
from profiles.repository import verify
from . import oauth2

router = APIRouter(
    prefix = "/verify",
    tags=["verify"]
)

get_db = db.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return await verify.create(db, current_user_email)
