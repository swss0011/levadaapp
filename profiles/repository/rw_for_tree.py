from fastapi import HTTPException
from profiles import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from sqlalchemy import literal
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


def delete(id: str, status_rw: str, db: Session, tree: Query):
    li = []

    print(id)
    print(status_rw)

    local_tree = tree.first()

    if status_rw == 'editor':
        print('in editor')
        li = list(local_tree.editors.split(","))
        print(li)
        if find_in_rw(li, id):
            print('in editor found')
            li.remove(id)
            tree.update({
                'editors': ','.join(str(e) for e in li)
            })
            db.commit()

    if status_rw == 'reader':
        print('in reader')
        li = list(local_tree.readers.split(","))
        print(li)
        if find_in_rw(li, id):
            print('in reader found')
            li.remove(id)
            tree.update({
                'readers': ','.join(str(e) for e in li)
            })
            db.commit()


def find_in_rw(li, id: str):
    return id in li


def destroy(request: schemas.TreeEditorsReaders, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id, models.TreeDb.owner == logged_in_user_id)

    util.check_tree_not_exist(tree)

    delete(request.id, request.status, db, tree)

    return {'msg': 'Done!!!'}


def get(request: schemas.TreeEditorsReadersView, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id, models.TreeDb.owner == logged_in_user_id)

    util.check_tree_not_exist(tree)

    li = []

    local_tree = tree.first()

    if request.status == 'editor':
        return {"editors": local_tree.editors}

    if request.status == 'reader':
        return {"readers": local_tree.readers}


def create(request: schemas.TreeEditorsReaders, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id, models.TreeDb.owner == logged_in_user_id)
    local_tree = tree.first()

    util.check_tree_not_exist(tree)
    user_for_rw = db.query(models.User).filter(models.User.id == request.id)
    util.check_user_not_found(user_for_rw)
    util.compare_owner_and_rw_ids(request.id, tree)
    util.contains_id_in_rwusers(request.id, request.status, tree)

    li = []

    if request.status == 'editor':
        if find_in_rw(list(local_tree.readers.split(",")), request.id):
            delete(request.id, 'reader', db, tree)
        li = list(local_tree.editors.split(","))
        li.append(request.id)
        tree.update({
            'editors': ','.join(str(e) for e in li)
        })

    if request.status == 'reader':
        if find_in_rw(list(local_tree.editors.split(",")), request.id):
            delete(request.id, 'editor', db, tree)
        li = list(local_tree.readers.split(","))
        li.append(request.id)
        tree.update({
            'readers': ','.join(str(e) for e in li)
        })

    db.commit()
    return tree.first()
