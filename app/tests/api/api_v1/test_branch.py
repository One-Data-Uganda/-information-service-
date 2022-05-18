import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app import app
from app.core.config import settings
from app.tests.utils.bank import create_random_bank, create_random_branch


@pytest.mark.asyncio
async def test_create_branch(faker, cache, client: TestClient, db: Session) -> None:
    bank = await create_random_bank(faker, cache, db)
    code = faker.numerify("BR###")
    name = faker.name()
    data = {"code": code, "name": name, "bank_id": bank.id}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post(
            f"{settings.API_V1_STR}/branch/",
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_branch = r.json()
        assert created_branch["name"] == name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post(
            f"{settings.API_V1_STR}/branch/",
            json=data,
        )
        assert r.status_code == 400
        created_branch = r.json()
        assert created_branch["message"] == "Branch with this ID already exists"


@pytest.mark.asyncio
async def test_get_existing_branch(
    faker, cache, client: TestClient, db: Session
) -> None:
    bank = await create_random_bank(faker, cache, db)
    branch = await create_random_branch(faker, cache, db, bank.id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/branch/{branch.id}",
        )
        assert 200 <= r.status_code < 300
        api_branch = r.json()
        assert api_branch["name"] == branch.name
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(
            f"{settings.API_V1_STR}/branch/0",
        )
        assert r.status_code == 404
        assert r.json()["message"] == "Branch not found"


@pytest.mark.asyncio
async def test_update_branch(faker, cache, client: TestClient, db: Session) -> None:
    bank = await create_random_bank(faker, cache, db)
    branch = await create_random_branch(faker, cache, db, bank.id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.put(
            f"{settings.API_V1_STR}/branch/{branch.id}", json={"name": faker.name()}
        )
        api_branch = r.json()
        print(api_branch)
        assert api_branch["id"] == branch.id
        assert api_branch["name"] != branch.name
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.put(f"{settings.API_V1_STR}/branch/0", json={"name": faker.name()})
        result = r.json()
        assert r.status_code == 404
        assert result["message"] == "Branch not found"


@pytest.mark.asyncio
async def test_find_branch(faker, cache, client: TestClient, db: Session) -> None:
    bank = await create_random_bank(faker, cache, db)
    branch = await create_random_branch(faker, cache, db, bank.id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/branch/{bank.id}/{branch.code}")
        api_branch = r.json()
        assert r.status_code == 200
        assert api_branch["code"] == branch.code

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get(f"{settings.API_V1_STR}/branch/bank/{bank.id}")
        api_branch = r.json()
        assert r.status_code == 200
        assert len(api_branch) > 0


# @pytest.mark.asyncio
# async def test_delete_branch(faker, cache, client: TestClient, db: Session) -> None:
#     bank = await create_random_bank(faker, cache, db)
#     branch = await create_random_branch(faker, cache, db, bank.id)
#     id = branch.id
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         r = await ac.delete(f"{settings.API_V1_STR}/branch/{id}")
#         api_branch = r.json()
#         print(api_branch)
#         assert r.status_code == 200
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         r = await ac.delete(f"{settings.API_V1_STR}/branch/0")
#         result = r.json()
#         print(result)
#         assert r.status_code == 404
#         assert result["message"] == "Branch not found"


# @pytest.mark.asyncio
# async def test_list_branches(faker, cache, client: TestClient, db: Session) -> None:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         r = await ac.get(f"{settings.API_V1_STR}/branch/")
#         api_branch = r.json()
#         assert r.status_code == 200
#         assert len(api_branch) > 0
