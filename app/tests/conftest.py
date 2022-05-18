import asyncio
import random
from typing import Generator

import pytest
from fakeredis import FakeStrictRedis
from fastapi.testclient import TestClient
from fastapi_plugins import depends_redis

from app import app
from app.db.session import SessionLocal
from app.tests.redis import redis_cache


@pytest.yield_fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def redis(monkeypatch):
    fake_redis = FakeStrictRedis()
    fake_redis.flushall()
    monkeypatch.setattr("celery_once.backends.redis.Redis.redis", fake_redis)
    return fake_redis


@pytest.fixture(scope="session")
async def cache() -> Generator:
    await redis_cache.init_cache()
    yield redis_cache


async def override_dependency():
    await redis_cache.init_cache()
    return redis_cache


app.dependency_overrides[depends_redis] = override_dependency


@pytest.fixture(scope="module")
def client() -> Generator:
    test_app = TestClient(app)
    yield test_app


@pytest.fixture(scope="session")
def db() -> Generator:
    db = SessionLocal()
    yield db


@pytest.fixture(autouse=True)
def faker_seed():
    r = int((random.SystemRandom(random.seed()).random()) * 100000000)
    return r
