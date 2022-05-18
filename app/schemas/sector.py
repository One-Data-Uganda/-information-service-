from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class SectorBase(BaseModel):
    id: Optional[str]
    sector_group_id: Optional[str]
    name: Optional[str]


# Properties to receive via API on creation
class SectorCreate(SectorBase):
    pass


class SectorUpdate(SectorBase):
    pass


class SectorInDBBase(SectorBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class Sector(SectorInDBBase):
    pass


# Additional properties stored in DB
class SectorInDB(SectorInDBBase):
    pass


class SectorResponse(BaseModel):
    success: bool
    data: Optional[Sector]


class SectorListResponse(BaseModel):
    success: bool
    data: Optional[List[Sector]]
