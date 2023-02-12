from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util, mail, random_code

def verify_email(code: str, db: Session):
    verify = db.query(models.VerifySingUp).filter(models.VerifySingUp.code == code)
    print('---verification_not_found')
    util.verification_not_found(verify)

    user_id = verify.first().user_id
    print('---db.query(models.User).filter')
    user = db.query(models.User).filter(models.User.id == user_id)
    print('---check_user_not_found_in_email_verification')
    util.check_user_not_found_in_email_verification(user)
    print('---timestring')
    timestring = verify.first().created_at

    util.check_expiration(timestring)

    username = user.first().username
    print('---user.update')
    user.update({'is_verified': True})
    db.commit()

    verify.delete(synchronize_session=False)
    db.commit()

    return {'msg': f'{username} is Verified!!!'}

async def password_change_request(email: str, db: Session):

    user = db.query(models.User).filter(models.User.email == email)

    util.check_user_not_found_in_email_verification(user)

    user_id = user.first().id

    randomCode = random_code.get_code()
    status_code = await mail.send_email(email, randomCode, False)

    util.check_email_status(status_code, email)

    found_change_password = db.query(models.ChangePassword).filter(models.ChangePassword.user_id == user_id)

    if found_change_password.first():
        found_change_password.delete(synchronize_session=False)
        db.commit()
    
    change_password = models.ChangePassword(code=randomCode, user_id=user_id)
    db.add(change_password)
    db.commit()
    db.refresh(change_password)

    return {'msg': f'Link to change password is sent to {email}!!!'}

async def create(db: Session, email: str):
    user = util.get_loginned_user(db, email)

    loginned_user_id = user.id
    util.check_user_is_not_verified(user.is_verified)

    verify = db.query(models.VerifySingUp).filter(models.VerifySingUp.user_id == loginned_user_id)

    if verify.first():
        verify.delete(synchronize_session=False)
        db.commit()

    await util.create_verification(db, email, loginned_user_id)

    return {'msg': f'Verification created!!!'}

    

