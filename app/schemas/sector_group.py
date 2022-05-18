from typing import List, Optional

from pydantic import BaseModel

from .sector import Sector


# Shared properties
class SectorGroupBase(BaseModel):
    id: Optional[str]
    name: str


# Properties to receive via API on creation
class SectorGroupCreate(SectorGroupBase):
    pass


class SectorGroupUpdate(SectorGroupBase):
    pass


class SectorGroupInDBBase(SectorGroupBase):
    sectors: Optional[List[Sector]]

    class Config:
        orm_mode = True


# Additional properties to return via API
class SectorGroup(SectorGroupInDBBase):
    pass


# Additional properties stored in DB
class SectorGroupInDB(SectorGroupInDBBase):
    pass


class SectorGroupResponse(BaseModel):
    success: bool
    data: Optional[SectorGroup]


class SectorGroupListResponse(BaseModel):
    success: bool
    data: Optional[List[SectorGroup]]
