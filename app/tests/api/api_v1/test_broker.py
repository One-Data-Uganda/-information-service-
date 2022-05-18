import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import app
from app.core.config import settings
from app.tests.utils.broker import create_random_broker

# from app.tests.utils.utils import


@pytest.mark.asyncio
async def test_list_brokers(faker, cache, db: Session) -> None:
    await create_random_broker(faker, cache, db)
    await create_random_broker(faker, cache, db)
    await create_random_broker(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/broker/")
        assert 200 <= r.status_code < 300
        results = r.json()
        assert len(results) >= 0


@pytest.mark.asyncio
async def test_get_existing_broker(faker, cache, db: Session) -> None:
    broker = await create_random_broker(faker, cache, db)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/broker/{broker.id}",
        )
        assert 200 <= r.status_code < 300
        api_broker = r.json()
        assert api_broker["name"] == broker.name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/broker/0",
        )
        assert r.status_code == 404
        assert r.json()["message"] == "Broker not found"
