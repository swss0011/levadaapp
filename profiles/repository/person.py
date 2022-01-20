from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util
from profiles.hashing import Hash
from fastapi import HTTPException
from . import helper

def show(current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.Person).filter(models.Person.owner == lined_user_id)

    return nodeInfo.all()


def destroy(id, current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.Person).filter(models.Person.id == id, models.Person.owner == lined_user_id)
    util.node_info_not_found("Node info", nodeInfo, id)

    nodeInfo.delete(synchronize_session=False)
    db.commit()
    return {'msg': 'Done!!!'}


def update(id, request: schemas.Person, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.Person).filter(models.Person.id == id, models.Person.owner == lined_user_id)
    util.node_info_not_found("Node info", nodeInfo, id)

    nodeInfo.update({
        'text': request.text,
        'search': request.search,
        'view': request.view
    })
    db.commit()
    return {'msg': 'Done!!!'}


def create(request: schemas.PersonCreate, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id)
    util.tree_not_found("Tree", tree, request.tree_id)

    owner_id = ""
    created_by = ""
    local_tree = tree.first()

    if helper.check_owner_of_tree(logged_in_user_id, tree):
        owner_id = logged_in_user_id
        created_by = logged_in_user_id
    else:
        util.check_user_is_editor(logged_in_user_id, tree)
        created_by = logged_in_user_id
        owner_id = local_tree.owner

    util.check_4_dates(request.date_of_birth_from, request.date_of_birth_to, request.date_of_death_from, request.date_of_death_to)

    date_of_birth_from = ""
    date_of_birth_to = ""
    date_of_death_from = ""
    date_of_death_to = ""

    count_birth = 0
    count_death = 0

    if request.date_of_birth_from:
        util.check_date(request.date_of_birth_from)
        date_of_birth_from = helper.get_date(request.date_of_birth_from)
        count_birth += 1

    if request.date_of_birth_to:
        util.check_date(request.date_of_birth_to)
        date_of_birth_to = helper.get_date(request.date_of_birth_to)
        count_birth += 1

    if request.date_of_death_from:
        util.check_date(request.date_of_death_from)
        date_of_death_from = helper.get_date(request.date_of_death_from)
        count_death += 1

    if request.date_of_death_to:
        util.check_date(request.date_of_death_to)
        date_of_death_to = helper.get_date(request.date_of_death_to)
        count_death += 1

    if count_birth == 1:
        if len(date_of_birth_from) > 1:
            date_of_birth_to = date_of_birth_from
        else:
            date_of_birth_from = date_of_birth_to

    if count_death == 1:
        if len(date_of_death_from) > 1:
            date_of_death_to = date_of_death_from
        else:
            date_of_death_from = date_of_death_to

    if count_death > 0 and count_death > 0:
        util.compare_dates(date_of_birth_to, date_of_death_from)


    #NEO4J!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    new_person = models.Person(
        owner_id = owner_id,
        tree_id = request.tree_id,
        created_by = created_by,
        node_from_neo4j_id = 1111111111111111111111111111111111111111111111111111111111111111,
        sex = request.sex,
        name = request.name,
        second_name = request.second_name,
        father_name = request.father_name,
        date_of_birth_from = date_of_birth_from,
        date_of_birth_to = date_of_birth_to,
        date_of_death_from = date_of_death_from,
        date_of_death_to = date_of_death_to,
        is_active = request.is_active,
        location = request.location,
        note = request.note,
        note_markdown = request.note_markdown,
        image = request.image
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person