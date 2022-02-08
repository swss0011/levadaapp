from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util
from profiles.hashing import Hash
from fastapi import HTTPException
from . import helper


def destroy(from_id, to_id, current_user_email: str, db: Session, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person_female = db.query(models.Person).filter(models.Person.id == from_id)
    util.person_not_found("Person", person_female, from_id)

    person_male = db.query(models.Person).filter(models.Person.id == to_id)
    util.person_not_found("Person", person_male, to_id)

    locale_person_female = person_female.first()
    locale_person_male = person_male.first()

    util.check_from_the_same_tree(locale_person_female.tree_id, locale_person_male.tree_id)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == locale_person_female.tree_id)
    util.tree_not_found("Tree", tree, locale_person_female.tree_id)

    helper.check_rights_for_node_and_edge(logged_in_user_id, tree)

    util.check_has_child_in_children(locale_person_male.id, person_female)

    util.check_no_mother(int(from_id), person_male)

    get_neo4j.delete_from_mother_to_son(locale_person_female.node_from_neo4j_id, locale_person_male.node_from_neo4j_id)


    helper.remove_id_from_parents(to_id, from_id, db)

    helper.delete_mother(person_male, db)

    return {'msg': 'Done!!!'}


def create(request: schemas.PersonEdge, db: Session, current_user_email: str, get_neo4j):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person_female = db.query(models.Person).filter(models.Person.id == request.from_id)
    util.person_not_found("Person", person_female, request.from_id)

    person_male = db.query(models.Person).filter(models.Person.id == request.to_id)
    util.person_not_found("Person", person_male, request.to_id)

    util.check_is_female(person_female)

    util.check_is_male(person_male)

    locale_person_female = person_female.first()
    locale_person_male = person_male.first()

    util.check_from_the_same_tree(locale_person_female.tree_id, locale_person_male.tree_id)

    tree = db.query(models.TreeDb).filter(models.TreeDb.id == locale_person_female.tree_id)
    util.tree_not_found("Tree", tree, locale_person_female.tree_id)

    helper.check_rights_for_node_and_edge(logged_in_user_id, tree)

    util.check_in_children(locale_person_male.id, person_female)

    util.check_has_mother(person_male)

    util.compare_dates_parent_child(locale_person_female.date_of_birth_from, locale_person_male.date_of_birth_to)

    get_neo4j.create_from_mother_to_son(locale_person_female.node_from_neo4j_id, locale_person_male.node_from_neo4j_id)

    helper.add_new_child(person_female, request.to_id, db)

    helper.add_mother(person_male, request.from_id, db)

    return {'msg': 'Done!!!'}