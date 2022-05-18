# Historical Index IndexPrices
import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class IndexPriceBase(BaseModel):
    index: str
    index_date: datetime.date
    value: float
    market_cap: float
    volume: float


# Properties to receive via API on creation
class IndexPriceCreate(IndexPriceBase):
    pass


class IndexPriceUpdate(IndexPriceBase):
    id: int
    pass


class IndexPriceInDBBase(IndexPriceBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class IndexPrice(IndexPriceInDBBase):
    pass


class IndexPriceRequestModel(BaseModel):
    index: Optional[str] = None
    start_date: datetime.date
    end_date: datetime.date
    callback: Optional[str] = None


class IndexPriceResponseModel(BaseModel):
    success: bool = True
    data: List[IndexPrice]
