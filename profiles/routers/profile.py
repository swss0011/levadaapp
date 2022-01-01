from typing import List
from fastapi import APIRouter, status, Depends
from profiles import db, schemas
from sqlalchemy.orm import Session
from profiles.repository import profile
from . import oauth2

router = APIRouter(
    prefix = "/profile",
    tags=["profile"]
)

get_db = db.get_db

@router.get('/', response_model=List[schemas.ShowProfile])
def all(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return profile.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Profile, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return profile.create(request, db, current_user_email)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return profile.destroy(id, db, current_user_email)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Profile, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return profile.update(id, request, db, current_user_email)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowProfile)
def show(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return profile.show(id, db)
