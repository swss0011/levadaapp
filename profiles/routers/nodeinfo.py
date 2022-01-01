from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import nodeinfo

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix="/nodeinfo",
    tags=["nodeinfo"]
)

get_db = db.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.NodeNote, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return nodeinfo.create(request, db, current_user_email)


@router.get('/', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return nodeinfo.show(current_user_email, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return nodeinfo.destroy(id, current_user_email, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.NodeNote, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return nodeinfo.update(id, request, db, current_user_email)
