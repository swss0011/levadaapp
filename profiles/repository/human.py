from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util

def get_all(db: Session):
    profiles = db.query(models.Profile).all()
    return profiles

def create(request: schemas.Profile, db: Session, email: str):
    user = util.get_loginned_user(db, email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    count_of_profiles = db.query(models.Profile).filter(models.Profile.user_id == loginned_user_id).count()

    util.check_count_of_profiles(count_of_profiles)

    new_profile = models.Profile(user_id=loginned_user_id, name=request.name, familyname=request.familyname)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def destroy(id, db: Session, email: str):
    user = util.get_loginned_user(db, email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    profile = db.query(models.Profile).filter(models.Profile.id == id, models.Profile.user_id == loginned_user_id)
    util.check_not_found("Profile", profile, id)

    profile.delete(synchronize_session=False)
    db.commit()
    return {'msg': 'Done!!!'}

def update(id, request: schemas.Profile, db: Session, email: str):
    user = util.get_loginned_user(db, email)
    loginned_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    profile = db.query(models.Profile).filter(models.Profile.id == id, models.Profile.user_id == loginned_user_id)
    util.check_not_found("Profile", profile, id)

    profile.update({'name': request.name, 'familyname': request.familyname})
    db.commit()
    return {'msg': 'Done!!!'}

def show(id, db: Session):
    profile = db.query(models.Profile).filter(models.Profile.id == id)
    util.check_not_found("Profile", profile, id)

    return profile.first()