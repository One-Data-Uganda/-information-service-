import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import app
from app.core.config import settings
from app.tests.utils.bank import create_random_bank, create_random_branch


@pytest.mark.asyncio
async def test_create_bank(faker, db: Session, cache, mocker) -> None:
    id = faker.numerify("BNK###")
    name = faker.name()
    data = {"id": id, "name": name}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post(
            f"{settings.API_V1_STR}/bank/",
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_bank = r.json()
        assert created_bank["name"] == name

    # Test existing bank
    name = faker.name()
    data = {"id": id, "name": name}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post(
            f"{settings.API_V1_STR}/bank/",
            json=data,
        )
        assert r.status_code == 400
        created_bank = r.json()
        assert created_bank["message"] == "Bank with this ID already exists"


@pytest.mark.asyncio
async def test_get_existing_bank(faker, db: Session, cache) -> None:
    print(cache)
    bank = await create_random_bank(faker, cache, db)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/bank/{bank.id}",
        )
        assert 200 <= r.status_code < 300
        api_bank = r.json()
        assert api_bank["name"] == bank.name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/bank/0",
        )
        assert r.status_code == 404
        assert r.json()["message"] == "Bank not found"


@pytest.mark.asyncio
async def test_retrieve_banks(faker, db: Session, cache) -> None:
    bank1 = await create_random_bank(faker, cache, db)
    bank2 = await create_random_bank(faker, cache, db)
    bank3 = await create_random_bank(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/bank/")

        all_banks = r.json()
        assert len(all_banks) > 3
        for item in all_banks:
            assert "id" in item


@pytest.mark.asyncio
async def test_update_bank(faker, db: Session, cache) -> None:
    bank = await create_random_bank(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.put(
            f"{settings.API_V1_STR}/bank/{bank.id}", json={"name": faker.name()}
        )

    api_bank = r.json()
    assert api_bank["id"] == bank.id
    assert api_bank["name"] != bank.name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.put(f"{settings.API_V1_STR}/bank/0", json={"name": faker.name()})

    result = r.json()
    assert r.status_code == 404
    assert result["message"] == "Bank not found"


@pytest.mark.asyncio
async def test_delete_bank(faker, db: Session, cache) -> None:
    bank = await create_random_bank(faker, cache, db)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.delete(f"{settings.API_V1_STR}/bank/{bank.id}")

    api_bank = r.json()
    print(api_bank)
    assert r.status_code == 200

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.delete(f"{settings.API_V1_STR}/bank/{bank.id}")

    result = r.json()
    assert r.status_code == 404
    assert result["message"] == "Bank not found"


@pytest.mark.asyncio
async def test_get_branches(faker, db: Session, cache) -> None:
    bank = await create_random_bank(faker, cache, db)
    branch1 = await create_random_branch(faker, cache, db, bank.id)
    branch2 = await create_random_branch(faker, cache, db, bank.id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/bank/{bank.id}/branches")

    api_bank = r.json()
    assert r.status_code == 200
    assert api_bank[0]["code"] == branch1.code or branch2.code
