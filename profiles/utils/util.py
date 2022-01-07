from fastapi import status, HTTPException
from sqlalchemy.orm.query import Query
from profiles.hashing import Hash
from profiles import schemas, models
from sqlalchemy.orm import Session
from . import random_code, mail
from datetime import datetime, timedelta
from dateutil import parser


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
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')


def check_user_not_found_in_email_verification(user: Query):
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found!!!')


def check_tree_exists(tree: Query):
    if tree.first():
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