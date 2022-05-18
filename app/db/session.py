from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

SQLAlchemyInstrumentor().instrument(
    engine=engine,
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
