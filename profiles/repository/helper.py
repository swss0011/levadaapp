from profiles import models, schemas
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

def remove_id_from_choldren(id, childrens, db: Session):
    li = list(childrens.split(","))

    for child_id in li:
        if child_id:
            child = int(child_id)
            remove_father_or_mother(child, id, db)

def remove_father_or_mother(child_id, parent_id, db: Session):
    child_node = db.query(models.Person).filter(models.Person.id == child_id)

    locale_child = child_node.first()

    mother_id = locale_child.mother_id
    father_id = locale_child.father_id

    if mother_id == parent_id:
        mother_id = 0
        child_node.update({
            'mother_id': mother_id
        })

        db.commit()

    if father_id == parent_id:
        father_id = 0
        child_node.update({
            'father_id': father_id
        })

        db.commit()


def get_person_born_date(id, db: Session):
    person = db.query(models.Person).filter(models.Person.id == id)
    local_person = person.first()
    return local_person.date_of_birth_to


def delete_person(person: Query, local_person, get_neo4j, db: Session):
    is_male = True
    if local_person.sex == "female":
        is_male = False

    get_neo4j.delete_person(str(id), is_male)

    mother_id = local_person.mother_id
    remove_id_from_parents(id, mother_id, db)

    father_id = local_person.father_id
    remove_id_from_parents(id, father_id, db)

    children_ids = local_person.children_ids
    remove_id_from_choldren(id, children_ids, db)

    person.delete(synchronize_session=False)
    db.commit()



def remove_id_from_parents(id, parent_id, db: Session):
    parents_node = db.query(models.Person).filter(models.Person.id == parent_id)

    parent = parents_node.first()

    children = parent.children_ids

    new_children = remove_id_from_list(children, id)

    parent.update({
        'children_ids': new_children
    })

    db.commit()


def remove_id_from_list(children, id):
    li = list(children.split(","))

    li.remove(str(id))
    return ','.join(str(e) for e in li)


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