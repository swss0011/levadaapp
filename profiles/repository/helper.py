from profiles import schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from profiles.utils import util
import re
from re import match

def check_owner_of_tree(id: str, tree: Query):
    local_tree = tree.first()

    return local_tree.owner == int(id)

def tree_exists(tree: Query):
    return tree.first()

def is_editor(id: str, tree: Query):
    local_tree = tree.first()

    li = list(local_tree.editors.split(","))
    return find_in_list(id, li)

def find_in_list(id, li):
    for item in li:
        if item:
            if int(item) == int(id):
                return True
    return False

def is_reader(id: str, tree: Query):
    local_tree = tree.first()

    li = list(local_tree.readers.split(","))
    print(f"Reader ID = {id}; TREE READERS = {li}; TREE ID = {local_tree.id}")
    return find_in_list(id, li)


def update_tree(db: Session, request: schemas.TreePut, tree: Query):
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