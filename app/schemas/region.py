from typing import List

from pydantic import BaseModel

from .sub_region import SubRegion


# Shared properties
class RegionBase(BaseModel):
    id: str


# Properties to receive via API on creation
class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    pass


class RegionInDBBase(RegionBase):
    subregions: List[SubRegion]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Region(RegionInDBBase):
    pass


# Additional properties stored in DB
class RegionInDB(RegionInDBBase):
    pass
