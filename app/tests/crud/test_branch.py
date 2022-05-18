import pytest
from sqlalchemy.orm import Session

from app import crud
from app.schemas.branch import BranchCreate
from app.tests.utils.bank import create_random_bank


@pytest.mark.asyncio
async def test_create_branch(faker, cache, db: Session) -> None:
    bank = await create_random_bank(faker, cache, db)

    code = faker.numerify("BR###")
    name = faker.name()
    branch_in = BranchCreate(code=code, name=name, bank_id=bank.id)
    branch = crud.branch.create(db=db, obj_in=branch_in)
    assert branch.code == code
    assert branch.name == name
    assert branch.id > 0
