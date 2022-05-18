from typing import List, Optional

from pydantic import BaseModel

from .sector_group import SectorGroup


# Shared properties
class SectorDivisionBase(BaseModel):
    id: Optional[str]
    name: str


# Properties to receive via API on creation
class SectorDivisionCreate(SectorDivisionBase):
    pass


class SectorDivisionUpdate(SectorDivisionBase):
    pass


class SectorDivisionInDBBase(SectorDivisionBase):
    groups: Optional[List[SectorGroup]]

    class Config:
        orm_mode = True


# Additional properties to return via API
class SectorDivision(SectorDivisionInDBBase):
    pass


# Additional properties stored in DB
class SectorDivisionInDB(SectorDivisionInDBBase):
    pass


class SectorDivisionResponse(BaseModel):
    success: bool
    data: Optional[SectorDivision]


class SectorDivisionListResponse(BaseModel):
    success: bool
    data: Optional[List[SectorDivision]]
