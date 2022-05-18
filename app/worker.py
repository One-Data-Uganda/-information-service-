from contextlib import contextmanager

import redis

from app.core.config import settings
from app.db.session import SessionLocal

redisConn = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
