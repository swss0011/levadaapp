from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import tree

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix="/tree",
    tags=["tree"]
)

get_db = db.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Tree, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return tree.create(request, db, current_user_email)


@router.get('/', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return tree.show(current_user_email, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return tree.destroy(id, current_user_email, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Tree, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return tree.update(id, request, db, current_user_email)
