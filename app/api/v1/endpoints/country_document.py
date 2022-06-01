import json
from typing import Any, List
from uuid import UUID

import aioredis
import fastapi_plugins
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.logger import TimedRoute, log  # noqa

router = APIRouter(route_class=TimedRoute)


@router.post("/", response_model=schemas.CountryDocument)
async def create_country_document(
    country_document_in: schemas.CountryDocumentCreate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Create new country_document.
    """
    try:
        country_document = crud.country_document.create(
            db=db, obj_in=country_document_in
        )
    except Exception:
        raise HTTPException(
            status_code=400, detail="CountryDocument with this ID already exists"
        )

    await cache.hset(
        "country_document", country_document.id, json.dumps(country_document.to_dict())
    )

    return {"success": True, "data": country_document}


@router.get("/{id}", response_model=schemas.CountryDocument)
async def get_country_document(
    id: UUID,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """Get country_document by ID."""
    r = crud.country_document.get(db, id)
    if not r:
        raise HTTPException(status_code=401, detail="CountryDocument not found")

    return {"success": True, "data": r}


@router.put("/{id}", response_model=schemas.CountryDocument)
async def update_country_document(
    id: UUID,
    country_document_in: schemas.CountryDocumentUpdate,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Update a country_document.
    """
    country_document = crud.country_document.get(db=db, id=id)
    if not country_document:
        raise HTTPException(status_code=404, detail="CountryDocument not found")

    country_document = crud.country_document.update(
        db=db, db_obj=country_document, obj_in=country_document_in
    )

    return {"success": True, "data": country_document}


@router.delete("/{id}", response_model=schemas.CountryDocument)
async def delete_country_document(
    id: UUID,
    db: Session = Depends(deps.get_db),
    cache: aioredis.Redis = Depends(fastapi_plugins.depends_redis),
) -> Any:
    """
    Delete an country_document.
    """
    country_document = crud.country_document.get(db=db, id=id)
    if not country_document:
        raise HTTPException(status_code=404, detail="CountryDocument not found")

    country_document = crud.country_document.remove(db=db, id=id)

    return {"success": True, "data": None}


@router.get("/{country_id}/list", response_model=List[schemas.CountryDocument])
async def list_country_documents(
    country_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve country_documents.
    """
    rows = crud.country_document.get_for_country(db, country_id)

    return {"success": True, "data": rows}


@router.get("/{id}/file")
def get_country_document_file(id: UUID, db: Session = Depends(deps.get_db)) -> Any:
    attachment = crud.amendment_attachment.get_file(db, id)

    if not attachment:
        raise HTTPException(status_code=404, detail="File not found")

    amendment = str(attachment["amendment_id"]).zfill(6)
    filename = f'USE Amendment {amendment} - Attachment - {attachment["attachment_type"]}.{attachment["extension"]}'

    return FileResponse(
        attachment["filepath"], media_type="application/octet-stream", filename=filename
    )
