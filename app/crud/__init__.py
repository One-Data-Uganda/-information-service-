from app.models import (
    Country,
    CountryContact,
    CountrySector,
    Region,
    Sector,
    SectorDivision,
    SectorGroup,
    SectorIndustry,
    SubRegion,
)
from app.schemas.country import CountryCreate, CountryUpdate
from app.schemas.country_contact import CountryContactCreate, CountryContactUpdate
from app.schemas.country_sector import CountrySectorCreate, CountrySectorUpdate
from app.schemas.region import RegionCreate, RegionUpdate
from app.schemas.sector import SectorCreate, SectorUpdate
from app.schemas.sector_division import SectorDivisionCreate, SectorDivisionUpdate
from app.schemas.sector_group import SectorGroupCreate, SectorGroupUpdate
from app.schemas.sector_industry import SectorIndustryCreate, SectorIndustryUpdate
from app.schemas.sub_region import SubRegionCreate, SubRegionUpdate

from .base import CRUDBase
from .crud_country_document import country_document  # noqa:F401

country = CRUDBase[Country, CountryCreate, CountryUpdate](Country)
country_contact = CRUDBase[CountryContact, CountryContactCreate, CountryContactUpdate](
    CountryContact
)
country_sector = CRUDBase[CountrySector, CountrySectorCreate, CountrySectorUpdate](
    CountrySector
)
sector = CRUDBase[Sector, SectorCreate, SectorUpdate](Sector)
sector_group = CRUDBase[SectorGroup, SectorGroupCreate, SectorGroupUpdate](SectorGroup)
sector_division = CRUDBase[SectorDivision, SectorDivisionCreate, SectorDivisionUpdate](
    SectorDivision
)
sector_industry = CRUDBase[SectorIndustry, SectorIndustryCreate, SectorIndustryUpdate](
    SectorIndustry
)
region = CRUDBase[Region, RegionCreate, RegionUpdate](Region)
sub_region = CRUDBase[SubRegion, SubRegionCreate, SubRegionUpdate](SubRegion)
