import json
from typing import Any

import aioredis
import fastapi_plugins
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.logger import TimedRoute, log  # noqa

router = APIRouter(route_class=TimedRoute)


@router.post("/", response_model=schemas.CountryResponse)
async def create_country(
    country_in: schemas.CountryCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new country.
    """
    try:
        country = crud.country.create(db=db, obj_in=country_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Country with this ID already exists"
        )

    await cache.hset("country", country.id, json.dumps(country.to_dict()))

    return {"success": True, "data": country}


@router.get("/{id}", response_model=schemas.CountryResponse)
async def get_country(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get country by ID."""
    r = crud.country.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="Country not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.CountryResponse)
async def update_country(
    id: str,
    country_in: schemas.CountryUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a country.
    """
    country = crud.country.get(db=db, id=id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    country = crud.country.update(db=db, db_obj=country, obj_in=country_in)

    return {"success": True, "data": country}


@router.delete("/{id}", response_model=schemas.CountryResponse)
async def delete_country(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an country.
    """
    country = crud.country.get(db=db, id=id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    country = crud.country.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/", response_model=schemas.CountryListResponse)
async def list_countrys(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve countrys.
    """
    rows = crud.country.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
