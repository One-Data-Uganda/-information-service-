from datetime import timedelta

from sqlalchemy.orm import Session

from app import crud
from app.models import Account, Transaction
from app.schemas.account import AccountCreate

from .bank import create_random_bank, create_random_branch

# id = Column(Integer, primary_key=True)
# account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'))
# broker_id = Column(CHAR(3))
# isin = Column(Text)
# qty = Column(BigInteger)
# creditdebit = Column(CHAR(4))
# type = Column(CHAR(4))
# transaction_date = Column(Date)
# dealprice = Column(Float(53))
# payment_ref = Column(Text)
# closing_balance = Column(BigInteger)
# payment_type = Column(Text)
# opening_balance = Column(BigInteger)
# stock = Column(Text)


def create_random_account(faker, db: Session) -> Account:
    bank = create_random_bank(faker, db)
    branch = create_random_branch(faker, db, bank.id)

    id = faker.numerify("X############")
    name = faker.name()
    mobile = faker.phone_number()
    address = faker.address()
    type = faker.random_element(("01", "02", "03"))
    dob = faker.past_date(start_date="-18y").strftime("%Y-%m-%d")
    box = faker.lexify("???")
    email = faker.email()
    id_no = faker.bothify(text="??##############??")
    country_id = "UG"
    bank_id = bank.id
    branch_code = branch.code
    gender = faker.random_element(("MALE", "FEMA"))
    account_number = faker.bban()

    account_in = AccountCreate(
        id=id,
        name=name,
        mobile=mobile,
        address=address,
        type=type,
        dob=dob,
        box=box,
        email=email,
        id_no=id_no,
        country_id=country_id,
        gender=gender,
        account_number=account_number,
        bank_id=bank_id,
        branch_code=branch_code,
    )

    return crud.account.create(db, obj_in=account_in)


def create_random_transaction(
    faker,
    db: Session,
    account_id: int,
    broker_id: str,
    stock: str,
    isin: str,
    prev_date: str = None,
    prev_id: int = 0,
    prevbal: int = 0,
) -> Transaction:
    if prev_id > 0:
        id = prev_id + 1
    else:
        id = faker.random_int(1, 9999)

    if prev_date is None:
        transaction_date = faker.past_date().strftime("%Y-%m-%d")
    else:
        transaction_date = (prev_date + timedelta(days=1)).strftime("%Y-%m-%d")

    if prevbal == 0:
        qty = faker.random_int(1, 9999999)
        creditdebit = "RECE"
    else:
        qty = faker.random_int(1, prevbal)
        creditdebit = faker.random_element(("RECE", "DELI"))

    type = "PLAC"
    dealprice = faker.random_int(1, 9999)
    payment_ref = faker.lexify("????????")
    if creditdebit == "RECE":
        closing_balance = prevbal + qty
    else:
        closing_balance = prevbal - qty
    stock = stock

    me = Transaction(
        id=id,
        account_id=account_id,
        broker_id=broker_id,
        isin=isin,
        qty=qty,
        creditdebit=creditdebit,
        type=type,
        transaction_date=transaction_date,
        dealprice=dealprice,
        payment_ref=payment_ref,
        closing_balance=closing_balance,
        opening_balance=prevbal,
        stock=stock,
    )
    db.add(me)
    db.commit()
    return me
