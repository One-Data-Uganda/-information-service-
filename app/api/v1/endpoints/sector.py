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


@router.post("/", response_model=schemas.SectorResponse)
async def create_sector(
    sector_in: schemas.SectorCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sector.
    """
    try:
        sector = crud.sector.create(db=db, obj_in=sector_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Sector with this ID already exists"
        )

    await cache.hset("sector", sector.id, json.dumps(sector.to_dict()))

    return {"success": True, "data": sector}


@router.get("/{id}", response_model=schemas.SectorResponse)
async def get_sector(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sector by ID."""
    r = crud.sector.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="Sector not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SectorResponse)
async def update_sector(
    id: str,
    sector_in: schemas.SectorUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sector.
    """
    sector = crud.sector.get(db=db, id=id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    sector = crud.sector.update(db=db, db_obj=sector, obj_in=sector_in)

    return {"success": True, "data": sector}


@router.delete("/{id}", response_model=schemas.SectorResponse)
async def delete_sector(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sector.
    """
    sector = crud.sector.get(db=db, id=id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    sector = crud.sector.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/", response_model=schemas.SectorListResponse)
async def list_sectors(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sectors.
    """
    rows = crud.sector.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
