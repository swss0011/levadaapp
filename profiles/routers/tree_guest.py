from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import tree_guest

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix="/tree_guest",
    tags=["tree guest"]
)

get_db = db.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def change(request: schemas.TreeForEditor, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return tree_guest.change(request, db, current_user_email)


@router.post('/show_trees/', status_code=status.HTTP_200_OK)
def show(request: schemas.ShowTreeForRW, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return tree_guest.show(request, db, current_user_email)
