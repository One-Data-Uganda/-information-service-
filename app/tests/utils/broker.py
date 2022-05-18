import json

from sqlalchemy.orm import Session

from app import crud
from app.models import Broker
from app.schemas.broker import BrokerCreate


async def create_random_broker(faker, cache, db: Session) -> Broker:
    id = faker.bothify("?##")
    fix_id = faker.lexify("?????")
    name = faker.name()
    enabled = faker.boolean()
    broker_in = BrokerCreate(id=id, name=name, fix_id=fix_id, enabled=enabled)
    r = crud.broker.create(db=db, obj_in=broker_in)
    await cache.hset("broker", r.id, json.dumps(r.to_dict()))
    return r
