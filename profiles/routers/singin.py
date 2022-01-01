from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from profiles import schemas, db, models
from profiles.utils import util, token
from profiles.repository import verify
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/login",
    tags=["login"]
)

get_db = db.get_db

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username)
    
    util.check_user_not_found(user)
    util.check_user_password(user, request)

    currentUser = user.first()
    access_token = token.create_access_token(data={"sub": currentUser.email})
    return {"access_token": access_token, "token_type": "bearer", "role": currentUser.role, "verified": currentUser.is_verified}

@router.get('/verifyemail/{code}', status_code=status.HTTP_200_OK)
def verify_email(code: str, db: Session = Depends(get_db)):
    return verify.verify_email(code, db)

@router.get('/pcr/{email}', status_code=status.HTTP_200_OK)
async def password_change_request(email: str, db: Session = Depends(get_db)):
    return await verify.password_change_request(email, db)
