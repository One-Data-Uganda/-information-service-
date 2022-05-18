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


@router.post("/", response_model=schemas.SectorClassResponse)
async def create_sector_class(
    sector_class_in: schemas.SectorClassCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sector_class.
    """
    try:
        sector_class = crud.sector_class.create(db=db, obj_in=sector_class_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="SectorClass with this ID already exists"
        )

    await cache.hset(
        "sector_class", sector_class.id, json.dumps(sector_class.to_dict())
    )

    return {"success": True, "data": sector_class}


@router.get("/{id}", response_model=schemas.SectorClassResponse)
async def get_sector_class(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sector_class by ID."""
    r = await cache.hget("sector_class", id)
    if r:
        return {"success": True, "data": json.loads(r)}

    r = crud.sector_class.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="SectorClass not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SectorClassResponse)
async def update_sector_class(
    id: str,
    sector_class_in: schemas.SectorClassUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sector_class.
    """
    sector_class = crud.sector_class.get(db=db, id=id)
    if not sector_class:
        raise HTTPException(status_code=404, detail="SectorClass not found")

    sector_class = crud.sector_class.update(
        db=db, db_obj=sector_class, obj_in=sector_class_in
    )

    await cache.hset(
        "sector_class", sector_class.id, json.dumps(sector_class.to_dict())
    )

    return {"success": True, "data": sector_class}


@router.delete("/{id}", response_model=schemas.SectorClassResponse)
async def delete_sector_class(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sector_class.
    """
    sector_class = crud.sector_class.get(db=db, id=id)
    if not sector_class:
        raise HTTPException(status_code=404, detail="SectorClass not found")

    sector_class = crud.sector_class.remove(db=db, id=id)

    await cache.hdel("sector_class", id)

    return {"success": True, "data": sector_class}


@router.get("/", response_model=schemas.SectorClassListResponse)
async def list_sector_classs(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sector_classs.
    """
    rows = crud.sector_class.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
