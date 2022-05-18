import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class CountryContactBase(BaseModel):
    country_id: Optional[str]
    govt_contact: Optional[str]
    economic_contact: Optional[str]
    parliament_contact: Optional[str]
    judiciary_contact: Optional[str]


# Properties to receive via API on creation
class CountryContactCreate(CountryContactBase):
    pass


class CountryContactUpdate(CountryContactBase):
    pass


class CountryContactInDBBase(CountryContactBase):
    id: int
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class CountryContact(CountryContactInDBBase):
    pass


# Additional properties stored in DB
class CountryContactInDB(CountryContactInDBBase):
    pass


class CountryContactResponse(BaseModel):
    success: bool
    data: Optional[CountryContact]


class CountryContactListResponse(BaseModel):
    success: bool
    data: Optional[List[CountryContact]]
