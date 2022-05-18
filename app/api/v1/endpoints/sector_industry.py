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


@router.post("/", response_model=schemas.SectorIndustryResponse)
async def create_sector_industry(
    sector_industry_in: schemas.SectorIndustryCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new sector_industry.
    """
    try:
        sector_industry = crud.sector_industry.create(db=db, obj_in=sector_industry_in)
    except Exception:
        raise HTTPException(
            status_code=400, detail="SectorIndustry with this ID already exists"
        )

    await cache.hset(
        "sector_industry", sector_industry.id, json.dumps(sector_industry.to_dict())
    )

    return {"success": True, "data": sector_industry}


@router.get("/{id}", response_model=schemas.SectorIndustryResponse)
async def get_sector_industry(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get sector_industry by ID."""
    r = await cache.hget("sector_industry", id)
    if r:
        return {"success": True, "data": json.loads(r)}

    r = crud.sector_industry.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="SectorIndustry not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.SectorIndustryResponse)
async def update_sector_industry(
    id: str,
    sector_industry_in: schemas.SectorIndustryUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a sector_industry.
    """
    sector_industry = crud.sector_industry.get(db=db, id=id)
    if not sector_industry:
        raise HTTPException(status_code=404, detail="SectorIndustry not found")

    sector_industry = crud.sector_industry.update(
        db=db, db_obj=sector_industry, obj_in=sector_industry_in
    )

    await cache.hset(
        "sector_industry", sector_industry.id, json.dumps(sector_industry.to_dict())
    )

    return {"success": True, "data": sector_industry}


@router.delete("/{id}", response_model=schemas.SectorIndustryResponse)
async def delete_sector_industry(
    id: str,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an sector_industry.
    """
    sector_industry = crud.sector_industry.get(db=db, id=id)
    if not sector_industry:
        raise HTTPException(status_code=404, detail="SectorIndustry not found")

    sector_industry = crud.sector_industry.remove(db=db, id=id)

    await cache.hdel("sector_industry", id)

    return {"success": True, "data": sector_industry}


@router.get("/", response_model=schemas.SectorIndustryListResponse)
async def list_sector_industries(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve sector_industrys.
    """
    rows = crud.sector_industry.get_multi(db, limit=1000)

    return {"success": True, "data": rows}
