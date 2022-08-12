from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

SQLAlchemyInstrumentor().instrument(
    engine=engine,
    pool_size=20,
    max_overflow=100,
    echo=False,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
