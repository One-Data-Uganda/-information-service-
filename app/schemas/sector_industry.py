from typing import List, Optional

from pydantic import BaseModel

from .sector_division import SectorDivision


# Shared properties
class SectorIndustryBase(BaseModel):
    id: Optional[str]
    name: str


# Properties to receive via API on creation
class SectorIndustryCreate(SectorIndustryBase):
    pass


class SectorIndustryUpdate(SectorIndustryBase):
    pass


class SectorIndustryInDBBase(SectorIndustryBase):
    divisions: Optional[List[SectorDivision]]

    class Config:
        orm_mode = True


# Additional properties to return via API
class SectorIndustry(SectorIndustryInDBBase):
    pass


# Additional properties stored in DB
class SectorIndustryInDB(SectorIndustryInDBBase):
    pass


class SectorIndustryResponse(BaseModel):
    success: bool
    data: SectorIndustry


class SectorIndustryListResponse(BaseModel):
    success: bool
    data: Optional[List[SectorIndustry]]
