import time

from faker import Faker
from sqlalchemy.orm import Session

from app import crud
from app.schemas.bank import BankCreate


def test_create_bank(faker, faker_seed, db: Session) -> None:
    id = faker.numerify("BNK###")
    name = faker.name()
    bank_in = BankCreate(id=id, name=name)
    bank = crud.bank.create(db=db, obj_in=bank_in)
    assert bank.name == name
    assert bank.id == id


def test_get_bank(faker, db: Session) -> None:
    Faker.seed(int(time.time() * 1000))
    id = faker.numerify("BNK###")
    name = faker.name()
    bank_in = BankCreate(id=id, name=name)
    bank = crud.bank.create(db=db, obj_in=bank_in)

    stored_bank = crud.bank.get(db=db, id=bank.id)
    assert stored_bank
    assert bank.id == stored_bank.id
    assert bank.name == stored_bank.name
