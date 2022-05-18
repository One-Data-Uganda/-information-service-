from pydantic import BaseModel

from .country import *  # noqa
from .country_contact import *  # noqa
from .country_document import *  # noqa
from .country_sector import *  # noqa
from .region import *  # noqa
from .sector import *  # noqa
from .sector_division import *  # noqa
from .sector_group import *  # noqa
from .sector_industry import *  # noqa
from .sub_region import *  # noqa


class FailureResponseModel(BaseModel):
    success: bool
    message: str
