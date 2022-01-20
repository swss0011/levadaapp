from profiles import schemas
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from profiles.utils import util
import re
from re import match

def get_date(date_str):
    pattern = r'^((?P<day>0[1-9]|[12][0-9]|3[01])[.](?P<month>0[1-9]|1[012])[.])?(?P<year>111[0-9]|11[2-9]\d|12\d\d|13\d\d|14\d\d|15\d\d|16\d\d|17\d\d|18\d\d|19\d\d|2\d{3}|30[0-3]\d|304[0-8])$'
    date_regex = re.compile(pattern)
    match = date_regex.search(date_str)
    day = 0
    month = 0
    year = 0
    if match:
        year = int(match.group("year"))
        if type(match.group("day")) is str and type(match.group("month")) is str:
            day = int(match.group("day"))
            month = int(match.group("month"))
        else:
            day = 1
            month = 1

    return f"{day}.{month}.{year}"

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