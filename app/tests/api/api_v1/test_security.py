import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import app
from app.core.config import settings
from app.tests.utils.security import create_random_security


@pytest.mark.asyncio
async def test_get_existing_security(faker, cache, db: Session) -> None:
    security = await create_random_security(faker, cache, db)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/security/{security.id}",
        )
        assert 200 <= r.status_code < 300
        api_security = r.json()
        assert api_security["name"] == security.name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/security/0",
        )
        assert r.status_code == 404
        assert r.json()["message"] == "Security not found"


@pytest.mark.asyncio
async def test_retrieve_securities(faker, cache, db: Session) -> None:
    security1 = await create_random_security(faker, cache, db)
    print(security1)
    security2 = await create_random_security(faker, cache, db)
    security3 = await create_random_security(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/security/")

    print(r)
    all_securitys = r.json()
    assert len(all_securitys) > 3
    for item in all_securitys:
        assert "id" in item


@pytest.mark.asyncio
async def test_retrieve_securities_by_type(faker, cache, db: Session) -> None:
    security1 = await create_random_security(faker, cache, db)
    security2 = await create_random_security(faker, cache, db)
    security3 = await create_random_security(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/security/list/{security1.security_type}"
        )

    print(r)
    all_securitys = r.json()
    assert len(all_securitys) > 0
    for item in all_securitys:
        assert "id" in item
