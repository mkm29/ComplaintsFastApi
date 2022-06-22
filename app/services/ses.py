import logging
from typing import List

import boto3
from fastapi import HTTPException

from app import settings


class SESService:
    def __init__(self):
        self.key = settings.aws_access_key_id
        self.secret = settings.aws_secret_access_key
        self.region = settings.aws_default_region
        if not self.key or not self.secret or not self.region:
            raise KeyError("Required AWS environment variables not found")

        self.ses_client = boto3.client(
            "ses",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region,
        )

    def send_mail(self, to_addresses: List[str], subject: str, body: str):
        try:
            response = self.ses_client.send_email(
                Destination={
                    "ToAddresses": to_addresses,
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": settings.charset,
                            "Data": body,
                        }
                    },
                    "Subject": {
                        "Charset": settings.charset,
                        "Data": subject,
                    },
                },
                Source=settings.from_email,
            )
        except Exception as exc:
            logging.error(exc)
            raise HTTPException(400, "There was an error sending the email")
        return response
