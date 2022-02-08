from fastapi import HTTPException
from profiles import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import literal
from profiles.utils import util
from . import helper


def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return profiles


def show(current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.owner == lined_user_id)

    return tree.all()


def destroy(id, current_user_email: str, db: Session, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == id, models.TreeDb.owner == lined_user_id)
    util.tree_not_found("Tree", tree, id)

    persons = db.query(models.Person).filter(models.Person.tree_id == id)

    locale_persons = persons.all()

    for per in locale_persons:
        person = db.query(models.Person).filter(models.Person.id == per.id)
        local_person = person.first()

        is_male = True
        if local_person.sex == "female":
            is_male = False
        get_neo4j.delete_person(local_person.node_from_neo4j_id, is_male)

        helper.delete_person(person, per, get_neo4j, db)

    tree.delete(synchronize_session=False)
    db.commit()
    return {'msg': 'Done!!!'}


def update(id, request: schemas.TreePut, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == id, models.TreeDb.owner == lined_user_id)
    util.tree_not_found("Tree", tree, id)

    trees_by_name = db.query(models.TreeDb).filter(models.TreeDb.name == request.name, models.TreeDb.owner == lined_user_id)
    util.check_tree_exists_by_id(trees_by_name, id)


    """
        if hasattr(request, 'notes'):
        if request.notes:
            if not request.name:
                tree.update({
                    'notes': request.notes,
                    'search': request.search,
                    'view': request.view
                })
            else:
                tree.update({
                    'name': request.name,
                    'notes': request.notes,
                    'search': request.search,
                    'view': request.view
                })
        else:
            if not request.name:
                tree.update({
                    'search': request.search,
                    'view': request.view
                })
            else:
                tree.update({
                    'name': request.name,
                    'search': request.search,
                    'view': request.view
                })

    db.commit()
    """

    helper.update_tree(db, request, tree)

    return {'msg': 'Done!!!'}

def find_and_search(request: schemas.TreeFindSearch, db: Session):
    tree = []

    if request.view == True and request.search == False:
        tree = db.query(models.TreeDb).filter(models.TreeDb.view == True, models.TreeDb.name.contains(request.text))

    if request.view == False and request.search == True:
        tree = db.query(models.TreeDb).filter(models.TreeDb.search == True, models.TreeDb.name.contains(request.text))

    if request.view == True and request.search == True:
        tree = db.query(models.TreeDb).filter(models.TreeDb.view == True, models.TreeDb.search == True, models.TreeDb.name.contains(request.text))

    if request.view == False and request.search == False:
        return tree

    return tree.all()



def create(request: schemas.Tree, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.name == request.name, models.TreeDb.owner == logged_in_user_id)
    util.check_tree_exists(tree)


    new_tree = models.TreeDb(
        name=request.name,
        owner=logged_in_user_id,
        search=request.search,
        view=request.view
    )
    db.add(new_tree)
    db.commit()
    db.refresh(new_tree)
    return new_tree