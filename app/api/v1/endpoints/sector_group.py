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


@router.post("/", response_model=schemas.SectorGroupResponse)
async def create_sector_group(
    sector_group_in: schemas.SectorGroupCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sector_group.
    """
    try:
        sector_group = crud.sector_group.create(db=db, obj_in=sector_group_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="SectorGroup with this ID already exists"
        )

    await cache.hset(
        "sector_group", sector_group.id, json.dumps(sector_group.to_dict())
    )

    return {"success": True, "data": sector_group}


@router.get("/{id}", response_model=schemas.SectorGroupResponse)
async def get_sector_group(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sector_group by ID."""
    r = await cache.hget("sector_group", id)
    if r:
        return {"success": True, "data": json.loads(r)}

    r = crud.sector_group.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="SectorGroup not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SectorGroupResponse)
async def update_sector_group(
    id: str,
    sector_group_in: schemas.SectorGroupUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sector_group.
    """
    sector_group = crud.sector_group.get(db=db, id=id)
    if not sector_group:
        raise HTTPException(status_code=404, detail="SectorGroup not found")

    sector_group = crud.sector_group.update(
        db=db, db_obj=sector_group, obj_in=sector_group_in
    )

    await cache.hset(
        "sector_group", sector_group.id, json.dumps(sector_group.to_dict())
    )

    return {"success": True, "data": sector_group}


@router.delete("/{id}", response_model=schemas.SectorGroupResponse)
async def delete_sector_group(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sector_group.
    """
    sector_group = crud.sector_group.get(db=db, id=id)
    if not sector_group:
        raise HTTPException(status_code=404, detail="SectorGroup not found")

    sector_group = crud.sector_group.remove(db=db, id=id)

    await cache.hdel("sector_group", id)

    return {"success": True, "data": sector_group}


@router.get("/", response_model=schemas.SectorGroupListResponse)
async def list_sector_groups(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sector_groups.
    """
    rows = crud.sector_group.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
