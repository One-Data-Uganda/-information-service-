import json

from sqlalchemy.orm import Session

from app import crud
from app.models import Bank, Branch
from app.schemas.bank import BankCreate
from app.schemas.branch import BranchCreate


async def create_random_bank(faker, cache, db: Session) -> Bank:
    id = faker.bothify("???###")
    name = faker.name()
    bank_in = BankCreate(id=id, name=name)
    r = crud.bank.create(db=db, obj_in=bank_in)
    await cache.hset("bank", r.id, json.dumps(r.to_dict()))
    return r


async def create_random_branch(faker, cache, db: Session, bank_id) -> Branch:
    code = faker.bothify("??###")
    name = faker.name()

    branch_in = BranchCreate(bank_id=bank_id, code=code, name=name)
    r = crud.branch.create(db=db, obj_in=branch_in)
    await cache.hset("branch", r.id, json.dumps(r.to_dict()))
    return r
