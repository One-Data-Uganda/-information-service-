import os
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.base import CRUDBase
from app.models import CountryDocument
from app.schemas.country_document import CountryDocumentCreate, CountryDocumentUpdate
from app.utils import decode_pdf, isBase64, uploadPDF


class CRUDCountryDocument(
    CRUDBase[CountryDocument, CountryDocumentCreate, CountryDocumentUpdate]
):
    def create(self, db: Session, obj_in: CountryDocumentCreate) -> Any:
        # Upload the file
        if not isBase64(obj_in.filename):
            return {
                "success": False,
                "message": "This is not a valid base64 encoded image",
            }

        attachment = decode_pdf(obj_in.filename)

        if not attachment:
            return {"success": False, "message": "This is not a valid PDF"}

        if not obj_in.id:
            obj_in.id = uuid.uuid4()

        attachment = uploadPDF(attachment, str(obj_in.id))

        obj_in.filesize = attachment["filesize"]

        r = super().create(db, obj_in=obj_in)

        db.commit()
        return r

    def get_file(self, db: Session, id: uuid.UUID) -> Any:
        attachment = self.get(db=db, id=id)
        if not attachment:
            return None

        filename = str(id)

        filepath = os.path.join(settings.UPLOADED_FILES_DEST, filename[:1], filename)
        return {"name": attachment.name, "filepath": filepath}


country_document = CRUDCountryDocument(CountryDocument)
