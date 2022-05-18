import base64
import io
import logging
import os
import uuid

import numpy as np
import phonenumbers
from PIL import Image
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app import crud, schemas
from app.core.config import settings
from app.core.logger import log
from app.db.session import SessionLocal
from app.models import Setting

max_tries = 60 * 5  # 5 minutes
wait_seconds = 15


def uuid_to_hex(uuid_string: str) -> str:
    """Turn uuid4 with dashes to hex

    From : 8791f25b-d4ca-4f10-8f60-407a507edefe
    To   : 8791f25bd4ca4f108f60407a507edefe

    :param uuid: uuid string with dashes
    :type uuid: str

    :returns: str - hex of uuid
    """

    return uuid.UUID(uuid_string).hex


def getSetting(key):
    try:
        db = SessionLocal()
        return db.query(Setting).get(key).value
    except Exception:
        return None


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.WARN),
)
def setSetting(key, value):
    try:
        db = SessionLocal()
        setting = db.query(Setting).get(key)
        setting.value = value
        db.commit()
    except Exception as e:
        log.error(e, exc_info=True)
        db.rollback()
        raise e


def uploadPhoto(f, name):
    try:
        image_data = np.asarray(f)
        image_data_bw = image_data.max(axis=2)
        non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
        non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
        cropBox = (
            min(non_empty_rows),
            max(non_empty_rows),
            min(non_empty_columns),
            max(non_empty_columns),
        )

        image_data_new = image_data[
            cropBox[0] : cropBox[1] + 1, cropBox[2] : cropBox[3] + 1, :
        ]

        new_image = Image.fromarray(image_data_new)
    except Exception:
        new_image = f

    # Need to overwrite if it exists
    filepath = os.path.join(settings.UPLOADED_FILES_DEST, name[:1], name)

    new_image.save(filepath, "png")
    thumb_image = Image.open(filepath)
    thumb_image.thumbnail((400, 400))
    thumb_image.save(f"{filepath}_thumb", "png")


def uploadPDF(pdf, name):
    # Need to overwrite if it exists
    filepath = os.path.join(settings.UPLOADED_FILES_DEST, name[:1], name)
    log.debug(f"writing to {filepath}")
    f = open(filepath, "wb")
    f.write(pdf)
    f.close()
    size = os.path.getsize(os.path.join(settings.UPLOADED_FILES_DEST, name[:1], name))

    return {"size": size}


def isBase64(sb):
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, "ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise False
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def decode_pdf(msg):
    try:
        bytes = base64.b64decode(msg, validate=True)
        log.debug(f"Got bytes [{bytes[0:4]}]")
        if bytes[0:4] != b"%PDF":
            return None
        return bytes
    except Exception as e:
        log.error(e, exc_info=True)
        return None


def decode_img(msg):
    try:
        msg = base64.b64decode(msg)
        buf = io.BytesIO(msg)
        img = Image.open(buf)
        return img
    except Exception:
        return None


def normalizeMSISDN(country, tel):
    try:
        r = phonenumbers.parse(tel, country)

        if phonenumbers.is_valid_number(r):
            return r.national_number
    except Exception:
        pass

    return None


def validateMSISDN(tel, country):
    try:
        r = phonenumbers.parse(tel, country)

        if phonenumbers.is_valid_number(r):
            return r
    except Exception:
        pass

    return None


def upload_image(db, id, image_data, type):
    if not image_data or image_data == "na":
        return {"success": True}

    data = schemas.ApplicationImageModel(data=image_data, type=type)

    application = crud.application.get(db=db, id=id)
    if not application:
        return {
            "success": False,
            "status_code": 404,
            "message": "Application not found",
        }

    if type == "id":
        fname = "attach_id"
        filename = application.attach_id
    elif type == "id_back":
        fname = "attach_id_back"
        filename = application.attach_id_back
    elif type == "photo":
        fname = "attach_photo"
        filename = application.attach_photo
    else:
        return {
            "success": False,
            "status_code": 422,
            "message": "`type` should be one of 'photo', 'id' or 'id_back'",
        }

    if not isBase64(image_data):
        return {
            "success": False,
            "status_code": 400,
            "message": "This is not a valid base64 encoded image",
        }

    picture = decode_img(image_data)

    if not picture:
        return {
            "success": False,
            "status_code": 400,
            "message": "This is not a valid image",
        }

    if not filename:
        filename = str(uuid.uuid4())

    uploadPhoto(picture, filename)

    r = crud.application.update(db=db, db_obj=application, obj_in={fname: filename})

    return {"success": True, "data": r}
