from fastapi import status, HTTPException
from sqlalchemy.orm.query import Query
from profiles.hashing import Hash
from profiles import schemas, models
from sqlalchemy.orm import Session
from . import random_code, mail
from datetime import datetime, timedelta
from dateutil import parser
import re
from re import match
import time


def get_loginned_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email)
    return user.first()


async def create_verification(db: Session, email: str, id: str):
    randomCode = random_code.get_code()
    status_code = await mail.send_email(email, randomCode)

    check_email_status(status_code, email)

    new_verify = models.VerifySingUp(user_id=id, code=randomCode)
    db.add(new_verify)
    db.commit()
    db.refresh(new_verify)


def verification_not_found(verification: Query):
    if not verification.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Check your email for latest verification')


def check_not_found(beginingOfSentence: str, profile: Query, id: str):
    if not profile.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')


def tree_not_found(beginingOfSentence: str, tree: Query, id: str):
    if not tree.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')


def node_info_not_found(beginingOfSentence: str, nodeInfo: Query, id: str):
    if not nodeInfo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')


def node_info_not_found(beginingOfSentence: str, nodeInfo: Query, id: str):
    if not nodeInfo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')


def check_user_not_found(user: Query):
    #print(user)
    #print('--------')
    #print(user.first())
    try:
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server: {ex}')



def check_user_not_found_in_email_verification(user: Query):
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found!!!')


def check_tree_exists(tree: Query):
    if tree.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Tree with name provided already exists')

def check_re_match(date_str):
    pattern = r'^((?P<day>0[1-9]|[12][0-9]|3[01])[.](?P<month>0[1-9]|1[012])[.])?(?P<year>111[0-9]|11[2-9]\d|12\d\d|13\d\d|14\d\d|15\d\d|16\d\d|17\d\d|18\d\d|19\d\d|2\d{3}|30[0-3]\d|304[0-8])$'
    date_regex = re.compile(pattern)
    match = date_regex.search(date_str)
    valid = False
    if match:
        return True
    return valid

def check_email(date_str):
    pattern = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
    date_regex = re.compile(pattern)
    match = date_regex.search(date_str)
    valid = False
    if match:
        return True

    if not valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Please check your email address')

def compare_dates_parent_child(date1, date2):
    if time.strptime(date1, "%d.%m.%Y") > time.strptime(date2, "%d.%m.%Y"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Child is older then Parent')


def verify_passwords(pass1: str, pass2: str):
    if pass1 != pass2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Password does not match')


def compare_dates_from_to(date1, date2):
    if time.strptime(date1, "%d.%m.%Y") > time.strptime(date2, "%d.%m.%Y"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Date FROM needs to be smaller then date TO')

def compare_dates(date1, date2):
    if time.strptime(date1, "%d.%m.%Y") > time.strptime(date2, "%d.%m.%Y"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Date of birth needs to be smaller then date of death')


def check_4_dates(born_from, born_to, end_from, end_to):
    if not check_re_match(born_from) and not check_re_match(born_to) and not check_re_match(end_from) and not check_re_match(end_to):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'At least one date needs to contain year or date (day.mont.year or year. For example: 30.12.2000; 2000). Now all 4 dates are not correct')

def check_date(any_date):
    if not check_re_match(any_date):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Needs to contain year or date (day.mont.year or year. For example: 30.12.2000; 2000). Now all 4 dates are not correct')


def check_user_is_editor(id: str, tree: Query):
    local_tree = tree.first()

    li = list(local_tree.editors.split(","))

    res = find_in_list(li, id)
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User can not edit the tree (name = {local_tree.name})')

def check_has_rights(has_rights):
    if not has_rights:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Does not have rights to perform changes')

def check_from_the_same_tree(from_tree_id: int, to_tree_id: int):
    if not from_tree_id == to_tree_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Persons from different trees')

def can_delete_node(owner,editor, tree: Query):
    local_tree = tree.first()

    if not owner and not editor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User can not delete the tree Nodes (name = {local_tree.name})')

def can_reader_nodes(owner,editor,reader, tree: Query):
    local_tree = tree.first()

    if not owner and not editor and not reader:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User can not read the tree Nodes (name = {local_tree.name})')

def check_is_female(person: Query):
    local_person = person.first()
    sex = local_person.sex

    if sex:
        if not sex == 'female':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not Female')

def check_is_male(person: Query):
    local_person = person.first()
    sex = local_person.sex

    print("in check_is_male")

    if sex:
        if not sex == 'male':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not Male')

def check_no_father(id: int, person: Query):
    local_person = person.first()
    father_id = local_person.father_id

    if not father_id == id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Does not have Father mentioned')

def check_no_mother(id: int, person: Query):
    #print(f"mother id = {id}")
    local_person = person.first()
    mother_id = local_person.mother_id

    #print(f"local_person.mother_id = {local_person.mother_id}")
    #print(f"type 1 = {type(id)} type2 = {type(mother_id)}")
    #print(f"mother_id == id ? {mother_id == id}")

    if not mother_id == id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Does not have Mother mentioned')


def check_has_father(person: Query):
    local_person = person.first()
    father_id = local_person.father_id

    if father_id:
        if father_id > 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Already has Father')

def check_has_mother(person: Query):
    local_person = person.first()
    mother_id = local_person.mother_id

    if mother_id:
        if mother_id > 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Already has Mother')

def check_has_child_in_children(id: str, person: Query):
    local_person = person.first()

    li = list(local_person.children_ids.split(","))

    res = find_in_list(li, id)
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Does not have the child')

def check_in_children(id: str, person: Query):
    local_person = person.first()

    li = list(local_person.children_ids.split(","))

    res = find_in_list(li, id)
    if res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Already connected as child')

def check_user_is_reader(id: str, tree: Query):
    local_tree = tree.first()

    li = list(local_tree.readers.split(","))

    res = find_in_list(li, id)
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User can not read the tree (name = {local_tree.name})')

def person_not_found(beginingOfSentence: str, person: Query, id: str):
    if not person.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')

def find_in_rw(li, id: str):
    return id in li

def find_in_list(li, id):
    li_str = list(map(int,filter(None,li)))

    for item in li_str:
        if item == int(id):
            return True
    return False

def check_tree_not_exist(tree: Query):
    if not tree.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Tree with name provided does not exist')

def compare_owner_and_rw_ids(id: str, tree: Query):
    local_tree = tree.first()

    if local_tree.owner == int(id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User is the owner of this tree')

def contains_id_in_rwusers(id: str, status_rw: str, tree: Query):
    local_tree = tree.first()
    li = []

    if status_rw == 'editor':
        li = list(local_tree.editors.split(","))

    if status_rw == 'reader':
        li = list(local_tree.readers.split(","))

    if id in li:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User exists in list')

def check_tree_exists_by_id(tree: Query, id: str):
    if tree.first():
        tree_by_name = tree.first()

        if int(id) != int(tree_by_name.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Tree with name provided already exists')

def check_user_exists(user: Query, email: str):
    if user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'User with {email} already exists')


def check_user_is_verified(is_verified: bool):
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Please check your email for verification message')


def check_user_is_not_verified(is_verified: bool):
    if is_verified:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Your registration is verified!!! No need to verify again')


def check_user_password(user: Query, request: schemas.Login):
    currentUser = user.first()
    if not Hash.verify(currentUser.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect Password')


def check_count_of_profiles(count_of_profiles: int):
    if count_of_profiles > 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Profile is available. User can have only one profile')


def check_change_password_exists(beginingOfSentence: str, changePassword: Query):
    id = changePassword.first().id
    if not changePassword.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{beginingOfSentence} with id {id} not found')


def check_email_status(status_code: int, email: str):
    if status_code != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Email to {email} with the link to change password was not sent')


def check_expiration(timeString: str):
    dateNow = datetime.now()
    createdAt = parser.parse(str(timeString))
    createdAtPlusExpirationTime = createdAt  + timedelta(hours=9)
    
    if dateNow > createdAtPlusExpirationTime:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=f'Expired!!!')