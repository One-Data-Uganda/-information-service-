import os
from csv import DictReader

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable

from app import models
from app.core.logger import log
from app.db import base  # noqa: F401
from app.db.session import engine


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def init_db(db: Session) -> None:
    log.info("initialising countries")
    # Create countries
    file_name = f"{os.getcwd()}/csv/country.csv"
    with open(file_name, "r") as f:
        dict_reader = DictReader(f)
        data = list(dict_reader)
        stmt = insert(models.Country).values(data)
        stmt = stmt.on_conflict_do_nothing(index_elements=[models.Country.id])
        db.execute(stmt)
        db.commit()

    log.info("initialising finished")


def drop_db(db: Session) -> None:
    db.close_all()
    base.Base.metadata.drop_all(bind=engine)
