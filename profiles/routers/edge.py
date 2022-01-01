from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import user

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix = "/edge",
    tags=["edge"]
)

get_db = db.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Edge, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    created = False
    
    user = util.get_loginned_user(db, current_user_email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    parent_exists = False
    child_exists = False

    if request.parent_gender == "male":
        parent_exists = neo4j_models.Male.nodes.get_or_none(
            first_name = request.parent_name,
            last_name = request.parent_familyname,
        )
    else:
        parent_exists = neo4j_models.Female.nodes.get_or_none(
            first_name = request.parent_name,
            last_name = request.parent_familyname,
        )

    if not parent_exists:
        raise HTTPException(status_code=400, detail="PARENT_DOES_NOT_EXIST")

    if request.child_gender == "male":
        child_exists = neo4j_models.Male.nodes.get_or_none(
            first_name = request.child_name,
            last_name = request.child_familyname,
        )
    else:
        child_exists = neo4j_models.Female.nodes.get_or_none(
            first_name = request.child_name,
            last_name = request.child_familyname,
        )

    if not child_exists:
        raise HTTPException(status_code=400, detail="CHILD_DOES_NOT_EXIST")

    
    try:
        if request.child_gender == "male":
            parent_exists.to_son.connect(child_exists)
            print("to son")
        else:
            parent_exists.to_daughter.connect(child_exists)
            print("to daughter")
    except:
        raise HTTPException(status_code=400, detail="IMPOSSIBLE_TO_CONNECT")

    
    return {'msg': 'Success'}
