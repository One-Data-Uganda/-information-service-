import datetime
from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class CountryBase(BaseModel):
    id: Optional[str]
    subregion_id: Optional[str]
    calling_code: Optional[int]
    name: Optional[str]
    other_names: Optional[str]
    motto: Optional[str]
    date_of_independence: Optional[datetime.date]
    introduction: Optional[str]
    location: Optional[str]
    neighbours: Optional[str]
    capital_city: Optional[str]
    population: Optional[float]
    languages: Optional[str]
    facts_and_figures: Optional[str]
    classification: Optional[str]
    life_expectancy: Optional[float]
    median_age: Optional[float]
    average_children: Optional[float]
    income_group: Optional[str]
    employment_rate: Optional[float]
    unemployment_rate: Optional[float]
    contribution_men: Optional[float]
    contribution_women: Optional[float]
    gdp_2019: Optional[float]
    gdp_per_capita: Optional[float]
    growth_of_gdp: Optional[float]
    inflation: Optional[float]
    investment: Optional[float]
    total_debt: Optional[float]
    gnp_per_capita: Optional[float]
    corruption_rank: Optional[float]
    credit_rank: Optional[float]
    business_score: Optional[float]
    key_sectors_growth: Optional[str]
    key_issues: Optional[str]


# Properties to receive via API on creation
class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryInDBBase(CountryBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class Country(CountryInDBBase):
    pass


# Additional properties stored in DB
class CountryInDB(CountryInDBBase):
    pass


class CountryResponse(BaseModel):
    success: bool
    data: Optional[Country]


class CountryListResponse(BaseModel):
    success: bool
    data: Optional[List[Country]]
