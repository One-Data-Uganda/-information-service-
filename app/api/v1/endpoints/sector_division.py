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


@router.post("/", response_model=schemas.SectorDivisionResponse)
async def create_sector_division(
    sector_division_in: schemas.SectorDivisionCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sector_division.
    """
    try:
        sector_division = crud.sector_division.create(db=db, obj_in=sector_division_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="SectorDivision with this ID already exists"
        )

    await cache.hset(
        "sector_division", sector_division.id, json.dumps(sector_division.to_dict())
    )

    return {"success": True, "data": sector_division}


@router.get("/{id}", response_model=schemas.SectorDivisionResponse)
async def get_sector_division(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sector_division by ID."""
    r = await cache.hget("sector_division", id)
    if r:
        return {"success": True, "data": json.loads(r)}

    r = crud.sector_division.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="SectorDivision not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SectorDivisionResponse)
async def update_sector_division(
    id: str,
    sector_division_in: schemas.SectorDivisionUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sector_division.
    """
    sector_division = crud.sector_division.get(db=db, id=id)
    if not sector_division:
        raise HTTPException(status_code=404, detail="SectorDivision not found")

    sector_division = crud.sector_division.update(
        db=db, db_obj=sector_division, obj_in=sector_division_in
    )

    await cache.hset(
        "sector_division", sector_division.id, json.dumps(sector_division.to_dict())
    )

    return {"success": True, "data": sector_division}


@router.delete("/{id}", response_model=schemas.SectorDivisionResponse)
async def delete_sector_division(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sector_division.
    """
    sector_division = crud.sector_division.get(db=db, id=id)
    if not sector_division:
        raise HTTPException(status_code=404, detail="SectorDivision not found")

    sector_division = crud.sector_division.remove(db=db, id=id)

    await cache.hdel("sector_division", id)

    return {"success": True, "data": sector_division}


@router.get("/", response_model=schemas.SectorDivisionListResponse)
async def list_sector_divisions(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sector_divisions.
    """
    rows = crud.sector_division.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
