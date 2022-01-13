from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import rw_for_tree

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix="/rwtree",
    tags=["reader or writer for tree"]
)

get_db = db.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.TreeEditorsReaders, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return rw_for_tree.create(request, db, current_user_email)

@router.post('/delete', status_code=status.HTTP_200_OK)
def desroy(request: schemas.TreeEditorsReaders, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return rw_for_tree.destroy(request, db, current_user_email)

@router.post('/get', status_code=status.HTTP_200_OK)
def get(request: schemas.TreeEditorsReadersView, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return rw_for_tree.get(request, db, current_user_email)

