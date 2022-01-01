from fastapi import APIRouter, status, Depends, HTTPException
from profiles import neo4j_models, schemas, db
from sqlalchemy.orm import Session
from profiles.repository import user

from profiles.utils import util
from . import oauth2

router = APIRouter(
    prefix = "/node",
    tags=["node"]
)

get_db = db.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Node, db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    created = False
    
    user = util.get_loginned_user(db, current_user_email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person_exists = False

    if request.gender == "male":
        person_exists = neo4j_models.Male.nodes.filter(
            first_name = request.name,
            last_name = request.familyname,
        )
        print(person_exists)
    else:
        person_exists = neo4j_models.Female.nodes.filter(
            first_name = request.name,
            last_name = request.familyname,
        )

    if person_exists:
        raise HTTPException(status_code=400, detail="USERNAME_TAKEN")

    if request.gender == "male":
        person_exists = neo4j_models.Male(first_name= request.name, last_name= request.familyname).save()
        created = True
    else:
        person_exists = neo4j_models.Female(first_name= request.name, last_name= request.familyname).save()
        created = True
    
    return {'msg': 'Success'}

@router.get('/', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db), current_user_email: str = Depends(oauth2.get_current_user)):
    created = False
    
    user = util.get_loginned_user(db, current_user_email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    dicNameToId = {}
    id_temp = 1

    nodes = []
    links = []

    for male in neo4j_models.Male.nodes:
        dicNameToId[male.first_name] = id_temp
        id_temp += 1

    for female in neo4j_models.Female.nodes:
        dicNameToId[female.first_name] = id_temp
        id_temp += 1

    id_temp = 1
    for male in neo4j_models.Male.nodes:
        nodes.append({
            'id': id_temp,
            'name': male.first_name
        })
        for mother in male.from_mother.all():
            links.append({
                'source': dicNameToId[mother.first_name],
                'target': dicNameToId[male.first_name]
            })
        for father in male.from_father.all():
            links.append({
                'source': dicNameToId[father.first_name],
                'target': dicNameToId[male.first_name]
            })
        id_temp += 1

    for female in neo4j_models.Female.nodes:
        nodes.append({
            'id': id_temp,
            'name': female.first_name
        })
        for mother in female.from_mother.all():
            links.append({
                'source': dicNameToId[mother.first_name],
                'target': dicNameToId[female.first_name]
            })
        for father in female.from_father.all():
            links.append({
                'source': dicNameToId[father.first_name],
                'target': dicNameToId[female.first_name]
            })
        id_temp += 1
    
    return {'nodes': nodes, 'links': links}
