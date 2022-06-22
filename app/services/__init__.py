import logging

from app.services.s3 import S3Service
from app.services.ses import SESService
from app.services.wise import WiseService

s3, ses, wise = None, None, None
try:
    s3 = S3Service()
    ses = SESService()
    wise = WiseService()
except Exception as exc:
    logging.error(exc)
