from typing import List

from pydantic import BaseModel

from .country import Country


# Shared properties
class SubRegionBase(BaseModel):
    id: str
    subregion_id: str


# Properties to receive via API on creation
class SubRegionCreate(SubRegionBase):
    pass


class SubRegionUpdate(SubRegionBase):
    pass


class SubRegionInDBBase(SubRegionBase):
    subregions: List[Country]

    class Config:
        orm_mode = True


# Additional properties to return via API
class SubRegion(SubRegionInDBBase):
    pass


# Additional properties stored in DB
class SubRegionInDB(SubRegionInDBBase):
    pass
