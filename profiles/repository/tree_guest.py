from fastapi import HTTPException
from profiles import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import literal
from profiles.utils import util
from . import helper


def show(request: schemas.ShowTreeForRW, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tres_for_response = []

    li = list(request.tree_ids.split(","))

    print(f"request.tree_ids = {request.tree_ids}")
    print(f"{li}")

    for id in li:
        if id:
            print(f"id = {id}")
            tree = db.query(models.TreeDb).filter(models.TreeDb.id == id)
            print(f"current tree {tree.first()}")
            if helper.tree_exists(tree):
                print(f"tree exists")
                if request.status == 'reader':
                    print(f"is reader")
                    if helper.is_reader(logged_in_user_id, tree):
                        print(f"update as reader")
                        tres_for_response.append(tree.first())
                if request.status == 'editor':
                    print(f"is editor")
                    if helper.is_editor(logged_in_user_id, tree):
                        print(f"update as editor")
                        tres_for_response.append(tree.first())


    return {"trees": tres_for_response}


def change(request: schemas.TreeForEditor, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id)
    util.tree_not_found("Tree", tree, request.tree_id)

    local_tree = tree.first()

    trees_by_name = db.query(models.TreeDb).filter(models.TreeDb.name == request.name, models.TreeDb.owner == local_tree.owner)
    util.check_tree_exists_by_id(trees_by_name, request.tree_id)

    util.check_user_is_editor(logged_in_user_id, tree)


    helper.update_tree(db, request, tree)

    return {'msg': 'Done!!!'}