from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.api import APICreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_api(db: Session, *, user_id: Optional[int] = None) -> models.API:
    if user_id is None:
        user = create_random_user(db)
        user_id = user.id
    name = random_lower_string()
    api_in = APICreate(user_id=user_id, name=name)
    return crud.api.create(db=db, obj_in=api_in)
