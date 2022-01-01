from fastapi import HTTPException
from profiles import models, schemas
from sqlalchemy.orm import Session
from profiles.utils import util


def show(current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.NodeNote).filter(models.NodeNote.owner == lined_user_id)

    return nodeInfo.all()


def destroy(id, current_user_email: str, db: Session):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.NodeNote).filter(models.NodeNote.id == id, models.NodeNote.owner == lined_user_id)
    util.node_info_not_found("Node info", nodeInfo, id)

    nodeInfo.delete(synchronize_session=False)
    db.commit()
    return {'msg': 'Done!!!'}


def update(id, request: schemas.Tree, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    lined_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    nodeInfo = db.query(models.NodeNote).filter(models.NodeNote.id == id, models.NodeNote.owner == lined_user_id)
    util.node_info_not_found("Node info", nodeInfo, id)

    nodeInfo.update({
        'text': request.text,
        'search': request.search,
        'view': request.view
    })
    db.commit()
    return {'msg': 'Done!!!'}


def create(request: schemas.Tree, db: Session, current_user_email: str):
    user = util.get_loginned_user(db, current_user_email)
    logged_in_user_id = user.id

    util.check_user_is_verified(user.is_verified)

    person_exists = False

    if person_exists:
        raise HTTPException(status_code=400, detail="USERNAME_TAKEN")

    new_node_info = models.NodeNote(
        text=request.text,
        node_id=request.node_id,
        tree_id=request.tree_id,
        owner=logged_in_user_id,
        search=request.search,
        view=request.view
    )
    db.add(new_node_info)
    db.commit()
    db.refresh(new_node_info)
    return new_node_info