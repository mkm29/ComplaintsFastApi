import base64
import logging
from typing import Optional

import aiohttp
import asyncio

from fastapi import HTTPException


def decode_photo(path: str, encoded_str: str):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_str.encode("utf-8")))
        except Exception as ex:
            logging.getLogger(__name__).error(ex)
            raise HTTPException(400, "Invalid photo encoding")


async def fetch(session, url: str, headers: Optional[dict] = None) -> dict:
    async with session.get(url, headers=headers) as response:
        return await response


async def post(session, url: str, data: dict, headers: Optional[dict] = None) -> dict:
    async with session.post(url, json=data, headers=headers) as response:
        return await response
