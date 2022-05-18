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


@router.post("/", response_model=schemas.SubRegion)
async def create_sub_region(
    sub_region_in: schemas.SubRegionCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sub_region.
    """
    try:
        sub_region = crud.sub_region.create(db=db, obj_in=sub_region_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="SubRegion with this ID already exists"
        )

    await cache.hset("sub_region", sub_region.id, json.dumps(sub_region.to_dict()))

    return {"success": True, "data": sub_region}


@router.get("/{id}", response_model=schemas.SubRegion)
async def get_sub_region(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sub_region by ID."""
    r = crud.sub_region.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="SubRegion not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SubRegion)
async def update_sub_region(
    id: str,
    sub_region_in: schemas.SubRegionUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sub_region.
    """
    sub_region = crud.sub_region.get(db=db, id=id)
    if not sub_region:
        raise HTTPException(status_code=404, detail="SubRegion not found")

    sub_region = crud.sub_region.update(db=db, db_obj=sub_region, obj_in=sub_region_in)

    return {"success": True, "data": sub_region}


@router.delete("/{id}", response_model=schemas.SubRegion)
async def delete_sub_region(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sub_region.
    """
    sub_region = crud.sub_region.get(db=db, id=id)
    if not sub_region:
        raise HTTPException(status_code=404, detail="SubRegion not found")

    sub_region = crud.sub_region.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/", response_model=List[schemas.SubRegion])
async def list_sub_regions(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sub_regions.
    """
    rows = crud.sub_region.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
