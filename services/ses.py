import logging
import os
from typing import List

import boto3
from fastapi import HTTPException

from constants import FROM_EMAIL, CHARSET


class SESService:
    def __init__(self):
        self.key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_DEFAULT_REGION")
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
                            "Charset": CHARSET,
                            "Data": body,
                        }
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": subject,
                    },
                },
                Source=FROM_EMAIL,
            )
        except Exception as exc:
            logging.error(exc)
            raise HTTPException(400, "There was an error sending the email")
        return response
