import json
from typing import Any, List

import aioredis
import fastapi_plugins
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.logger import TimedRoute, log  # noqa

router = APIRouter(route_class=TimedRoute)


@router.post("/", response_model=schemas.CountryContact)
async def create_country_contact(
    country_contact_in: schemas.CountryContactCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new country_contact.
    """
    try:
        country_contact = crud.country_contact.create(db=db, obj_in=country_contact_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="CountryContact with this ID already exists"
        )

    await cache.hset(
        "country_contact", country_contact.id, json.dumps(country_contact.to_dict())
    )

    return {"success": True, "data": country_contact}


@router.get("/{id}", response_model=schemas.CountryContact)
async def get_country_contact(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get country_contact by ID."""
    r = crud.country_contact.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="CountryContact not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.CountryContact)
async def update_country_contact(
    id: str,
    country_contact_in: schemas.CountryContactUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a country_contact.
    """
    country_contact = crud.country_contact.get(db=db, id=id)
    if not country_contact:
        raise HTTPException(status_code=404, detail="CountryContact not found")

    country_contact = crud.country_contact.update(
        db=db, db_obj=country_contact, obj_in=country_contact_in
    )

    return {"success": True, "data": country_contact}


@router.delete("/{id}", response_model=schemas.CountryContact)
async def delete_country_contact(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an country_contact.
    """
    country_contact = crud.country_contact.get(db=db, id=id)
    if not country_contact:
        raise HTTPException(status_code=404, detail="CountryContact not found")

    country_contact = crud.country_contact.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/", response_model=List[schemas.CountryContact])
async def list_country_contacts(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve country_contacts.
    """
    rows = crud.country_contact.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
