from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util
from profiles.hashing import Hash
from fastapi import HTTPException
from . import helper

def show(tree_id, current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == tree_id)
    util.tree_not_found("Tree", tree, tree_id)

    local_tree = tree.first()

    util.can_reader_nodes(
        helper.check_owner_of_tree(logged_in_user_id, tree),
        helper.is_editor(logged_in_user_id, tree),
        helper.is_reader(logged_in_user_id, tree),
        tree)

    nodes = db.query(models.Person).filter(models.Person.tree_id == tree_id)

    return nodes.all()


def destroy(id, current_user_email: str, db: Session, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person = db.query(models.Person).filter(models.Person.id == id)
    util.person_not_found("Person", person, id)

    local_person = person.first()
    tree_id = local_person.tree_id

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == tree_id)
    util.tree_not_found("Tree", tree, tree_id)

    local_tree = tree.first()

    util.can_delete_node(
        helper.check_owner_of_tree(logged_in_user_id, tree),
        helper.is_editor(logged_in_user_id, tree),
        tree)

    is_male = True
    if local_person.sex == "female":
        is_male = False

    get_neo4j.delete_person(local_person.node_from_neo4j_id, is_male)

    helper.delete_person(person, local_person, get_neo4j, db)

    return {'msg': 'Done!!!'}


def update(id, request: schemas.PersonUpdate, db: Session, current_user_email: str, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person = db.query(models.Person).filter(models.Person.id == id)
    util.person_not_found("Person", person, id)

    local_person = person.first()
    tree_id = local_person.tree_id

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == tree_id)
    util.tree_not_found("Tree", tree, tree_id)

    owner_id = ""
    created_by = ""
    is_life = request.is_active

    local_tree = tree.first()

    if helper.check_owner_of_tree(logged_in_user_id, tree):
        owner_id = logged_in_user_id
        created_by = logged_in_user_id
    else:
        util.check_user_is_editor(logged_in_user_id, tree)
        created_by = logged_in_user_id
        owner_id = local_tree.owner

    #util.check_4_dates(request.date_of_birth_from, request.date_of_birth_to, request.date_of_death_from, request.date_of_death_to)

    name = local_person.name
    location = local_person.location

    is_active_db = local_person.is_active

    second_name = local_person.second_name
    father_name = local_person.father_name

    note = local_person.note
    note_markdown = local_person.note_markdown
    image = local_person.image

    if len(request.name) > 0:
        name = request.name

    if len(request.location) > 0:
        location = request.location

    if len(request.second_name) > 0:
        second_name = request.second_name

    if len(request.father_name) > 0:
        father_name = request.father_name

    if len(request.note) > 0:
        note = request.note

    if len(request.note_markdown) > 0:
        note_markdown = request.note_markdown

    if len(request.image) > 0:
        image = request.image

    date_of_birth_from = local_person.date_of_birth_from
    date_of_birth_to = local_person.date_of_birth_to
    date_of_death_from = local_person.date_of_death_from
    date_of_death_to = local_person.date_of_death_to

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

    is_death_from = True

    if request.date_of_death_from:
        util.check_date(request.date_of_death_from)
        date_of_death_from = helper.get_date(request.date_of_death_from)
        count_death += 1

    if request.date_of_death_to:
        util.check_date(request.date_of_death_to)
        date_of_death_to = helper.get_date(request.date_of_death_to)
        count_death += 1
        is_death_from = False

    if count_death == 1:
        if is_death_from:
            if len(date_of_death_to) == 0:
                date_of_death_to = date_of_death_from
        if not is_death_from:
            if len(date_of_death_from) == 0:
                date_of_death_from = date_of_death_to

    if count_birth > 0:
        util.compare_dates_from_to(date_of_birth_from, date_of_birth_to)

    if count_death > 0:
        util.compare_dates_from_to(date_of_death_from, date_of_death_to)

    if len(date_of_death_from) > 0 and count_birth > 0:
        util.compare_dates(date_of_birth_to, date_of_death_from)

    if len(date_of_death_from) > 0:
        is_life = False



    mother_id = local_person.mother_id
    father_id = local_person.father_id
    date_person_born = helper.get_date(date_of_birth_to)

    if mother_id > 0 or father_id > 0:
        if mother_id > 0:
            mother_born = helper.get_person_born_date(mother_id, db)
            date_mother_born = helper.get_date(mother_born)
            util.compare_dates(date_person_born, date_mother_born)
        if father_id > 0:
            father_born = helper.get_person_born_date(father_id, db)
            date_father_born = helper.get_date(father_born)
            util.compare_dates(date_person_born, date_father_born)

    li = list(local_person.children_ids.split(","))

    for child in li:
        if child:
            child_born = helper.get_person_born_date(int(child), db)
            date_child_born = helper.get_date(child_born)
            util.compare_dates(date_child_born, date_person_born)

    #UPDATE NEO4J NAME!!!
    neo4j_new_name = f"{request.second_name} {request.name} {request.father_name}"
    neo4j_old_name = f"{local_person.second_name} {local_person.name} {local_person.father_name}"
    if not neo4j_new_name == neo4j_old_name:
        get_neo4j.change_name(local_person.node_from_neo4j_id, neo4j_new_name)

    person.update({
        'name': name,
        'second_name': second_name,
        'father_name': father_name,
        'date_of_birth_from': date_of_birth_from,
        'date_of_birth_to': date_of_birth_to,
        'date_of_death_from': date_of_death_from,
        'date_of_death_to': date_of_death_to,
        'is_active': is_life,
        'note': request.note,
        'location': location,
        'note_markdown': note_markdown,
        'image': image,
    })
    db.commit()
    return {'msg': 'Done!!!'}


def create(request: schemas.PersonCreate, db: Session, current_user_email: str, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == request.tree_id)
    util.tree_not_found("Tree", tree, request.tree_id)

    owner_id = ""
    created_by = ""
    is_life = request.is_active

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

    if count_birth == 2:
        util.compare_dates_from_to(date_of_birth_from, date_of_birth_to)

    if count_death == 2:
        util.compare_dates_from_to(date_of_death_from, date_of_death_to)

    if count_death > 0 and count_birth > 0:
        util.compare_dates(date_of_birth_to, date_of_death_from)

    if count_death > 0:
        is_life = False

    is_male = True
    if request.sex == "female":
        is_male = False
    neo4j_id = get_neo4j.create_person(f"{request.second_name} {request.name} {request.father_name}", is_male)


    new_person = models.Person(
        owner_id = owner_id,
        tree_id = request.tree_id,
        created_by = created_by,
        node_from_neo4j_id = neo4j_id,
        sex = request.sex,
        name = request.name,
        second_name = request.second_name,
        father_name = request.father_name,
        date_of_birth_from = date_of_birth_from,
        date_of_birth_to = date_of_birth_to,
        date_of_death_from = date_of_death_from,
        date_of_death_to = date_of_death_to,
        is_active = is_life,
        location = request.location,
        note = request.note,
        note_markdown = request.note_markdown,
        image = request.image
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person