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


@router.post("/", response_model=schemas.CountrySector)
async def create_country_sector(
    country_sector_in: schemas.CountrySectorCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new country_sector.
    """
    try:
        country_sector = crud.country_sector.create(db=db, obj_in=country_sector_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="CountrySector with this ID already exists"
        )

    await cache.hset(
        "country_sector", country_sector.id, json.dumps(country_sector.to_dict())
    )

    return {"success": True, "data": country_sector}


@router.get("/{id}", response_model=schemas.CountrySector)
async def get_country_sector(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get country_sector by ID."""
    r = crud.country_sector.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="CountrySector not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.CountrySector)
async def update_country_sector(
    id: str,
    country_sector_in: schemas.CountrySectorUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a country_sector.
    """
    country_sector = crud.country_sector.get(db=db, id=id)
    if not country_sector:
        raise HTTPException(status_code=404, detail="CountrySector not found")

    country_sector = crud.country_sector.update(
        db=db, db_obj=country_sector, obj_in=country_sector_in
    )

    return {"success": True, "data": country_sector}


@router.delete("/{id}", response_model=schemas.CountrySector)
async def delete_country_sector(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an country_sector.
    """
    country_sector = crud.country_sector.get(db=db, id=id)
    if not country_sector:
        raise HTTPException(status_code=404, detail="CountrySector not found")

    country_sector = crud.country_sector.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/", response_model=List[schemas.CountrySector])
async def list_country_sectors(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve country_sectors.
    """
    rows = crud.country_sector.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
