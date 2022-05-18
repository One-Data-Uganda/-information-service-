from fastapi import APIRouter

from app.api.v1.endpoints import (
    country,
    country_contact,
    country_document,
    country_sector,
    region,
    sector,
    sector_division,
    sector_group,
    sector_industry,
    sub_region,
)

api_router = APIRouter()
api_router.include_router(country.router, prefix="/country", tags=["country"])
api_router.include_router(
    country_document.router, prefix="/country-document", tags=["country document"]
)
api_router.include_router(
    country_sector.router, prefix="/country-sector", tags=["country sector"]
)
api_router.include_router(
    country_contact.router, prefix="/country-contact", tags=["country contact"]
)
api_router.include_router(sector.router, prefix="/sector", tags=["sector"])
api_router.include_router(
    sector_group.router, prefix="/sector-group", tags=["sector group"]
)
api_router.include_router(
    sector_division.router, prefix="/sector-division", tags=["sector division"]
)
api_router.include_router(
    sector_industry.router, prefix="/sector-industry", tags=["sector industry"]
)
api_router.include_router(region.router, prefix="/region", tags=["region"])
api_router.include_router(sub_region.router, prefix="/sub-region", tags=["sub region"])
