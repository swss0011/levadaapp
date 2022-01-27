from fastapi import APIRouter, status, Depends
from profiles import schemas, db
from sqlalchemy.orm import Session
from profiles.repository import from_father_to_son

from . import oauth2

router = APIRouter(
    prefix = "/fromFatherToSon",
    tags=["Edge From Father To Son"]
)

get_db = db.get_db

get_neo4j = db.get_neo4j()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.PersonEdge, db: Session = Depends(get_db),
           current_user_email: str = Depends(oauth2.get_current_user)):
    return from_father_to_son.create(request, db, current_user_email, get_neo4j)


@router.delete('/{from_id}/{to_id}', status_code=status.HTTP_204_NO_CONTENT)
def desroy(from_id, to_id, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    return from_father_to_son.destroy(from_id, to_id, current_user_email, db, get_neo4j)
