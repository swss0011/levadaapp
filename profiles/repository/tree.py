from fastapi import HTTPException
from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util


def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return profiles


def show(current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.owner == lined_user_id)

    return tree.all()


def destroy(id, current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == id, models.TreeDb.owner == lined_user_id)
    util.tree_not_found("Tree", tree, id)

    tree.delete(synchronize_session=False)
    db.commit()
    return {'msg': 'Done!!!'}


def update(id, request: schemas.Tree, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == id, models.TreeDb.owner == lined_user_id)
    util.tree_not_found("Tree", tree, id)

    if hasattr(request, 'notes'):
        if request.notes:
            tree.update({
                'name': request.name,
                'notes': request.notes,
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
    return {'msg': 'Done!!!'}


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