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


@router.post("/", response_model=schemas.Region)
async def create_region(
    region_in: schemas.RegionCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new region.
    """
    try:
        region = crud.region.create(db=db, obj_in=region_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Region with this ID already exists"
        )

    await cache.hset("region", region.id, json.dumps(region.to_dict()))

    return region


@router.get("/{id}", response_model=schemas.Region)
async def get_region(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get region by ID."""
    r = await cache.hget("region", id)
    if r:
        return json.loads(r)

    r = crud.region.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="Region not found")

    return r


@router.put("/{id}", response_model=schemas.Region)
async def update_region(
    id: str,
    region_in: schemas.RegionUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a region.
    """
    region = crud.region.get(db=db, id=id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region = crud.region.update(db=db, db_obj=region, obj_in=region_in)

    await cache.hset("region", region.id, json.dumps(region.to_dict()))

    return region


@router.delete("/{id}", response_model=schemas.Region)
async def delete_region(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an region.
    """
    region = crud.region.get(db=db, id=id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region = crud.region.remove(db=db, id=id)

    await cache.hdel("region", id)

    return region


@router.get("/", response_model=List[schemas.Region])
async def list_regions(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve countries.
    """
    rows = crud.region.get_multi(db, limit=1000)

    return rows
