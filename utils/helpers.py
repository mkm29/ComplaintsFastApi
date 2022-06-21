import base64
import logging
from fastapi import HTTPException


def decode_photo(path: str, encoded_str: str):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_str.encode("utf-8")))
        except Exception as ex:
            logging.getLogger(__name__).error(ex)
            raise HTTPException(400, "Invalid photo encoding")
