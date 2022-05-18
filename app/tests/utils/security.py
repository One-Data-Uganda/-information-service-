import json

from sqlalchemy.orm import Session

from app.models import Security


async def create_random_security(faker, cache, db: Session) -> Security:
    me = Security(
        id=faker.lexify("??????"),
        security_type=faker.bothify("???###"),
        name=faker.name(),
        code=faker.bothify("???###"),
        factor=faker.random_int(),
        multiplier=faker.random_int(),
        increment=faker.random_int(),
    )
    db.add(me)
    db.commit()
    await cache.hset("security", me.id, json.dumps(me.to_dict()))
    return me
