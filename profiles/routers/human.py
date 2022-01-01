from typing import List
from fastapi import APIRouter, status, Depends
from profiles import db, schemas
from sqlalchemy.orm import Session
from profiles.repository import human
from . import oauth2

router = APIRouter(
    prefix = "/human",
    tags=["human"]
)

get_db = db.get_db

@router.get('/', response_model=List[schemas.Human])
def all(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return human.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Human, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return human.create(request, db, current_user_email)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return human.destroy(id, db, current_user_email)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Human, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return human.update(id, request, db, current_user_email)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Human)
def show(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return human.show(id, db)
