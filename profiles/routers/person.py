from fastapi import APIRouter, status, Depends
from profiles import schemas, db
from sqlalchemy.orm import Session
from profiles.repository import person

from . import oauth2

router = APIRouter(
    prefix = "/person",
    tags=["person"]
)

get_db = db.get_db

get_neo4j = db.get_neo4j()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.PersonCreate, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return person.create(request, db, current_user_email, get_neo4j)


@router.get('/{tree_id}', status_code=status.HTTP_200_OK)
def all(tree_id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return person.show(tree_id, current_user_email, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return person.destroy(id, current_user_email, db, get_neo4j)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.PersonUpdate, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return person.update(id, request, db, current_user_email)