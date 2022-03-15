from fastapi import APIRouter, status, Depends
from profiles import schemas, db
from sqlalchemy.orm import Session
from profiles.repository import user

router = APIRouter(
    prefix = "/user",
    tags=["user"]
)

get_db = db.get_db

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def create_user(request: schemas.UserSingUp, db: Session = Depends(get_db)):
    return await user.create_user(request, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show(id, db: Session = Depends(get_db)):
    return user.show(id, db)

@router.put('/changepasword/{code}', status_code=status.HTTP_202_ACCEPTED)
def change_pasword(request: schemas.UserPass, code: str, db: Session = Depends(get_db)):
    return user.update_password(request, code, db)