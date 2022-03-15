from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util
from profiles.hashing import Hash

async def create_user(request: schemas.UserSingUp, db: Session):
    util.verify_passwords(request.password, request.second_password)

    user = db.query(models.User).filter(models.User.email == request.email)

    util.check_user_exists(user, request.email)

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(new_user.id)

    util.check_email(request.email)

    await util.create_verification(db, request.email, new_user.id)

    return new_user

def show(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    util.check_not_found("User", user, id)

    return user.first()

def update_password(request: schemas.UserPass, code: str, db: Session):
    changePassword = db.query(models.ChangePassword).filter(models.ChangePassword.code == code)
    util.check_change_password_exists("Change password request", changePassword)

    user_id = changePassword.first().user_id

    user = db.query(models.User).filter(models.User.id == user_id)
    util.check_not_found("User", user, user_id)

    timestring = changePassword.first().created_at

    util.check_expiration(timestring)

    username = user.first().username

    #models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))

    user.update({'password': Hash.bcrypt(request.password)})
    db.commit()

    changePassword.delete(synchronize_session=False)
    db.commit()

    return {'msg': f'Password for {username} is changed!!!'}