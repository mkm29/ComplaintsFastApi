import logging
from os.path import basename
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app import settings


class S3Service:
    def __init__(self):
        self.key = settings.aws_access_key_id
        self.secret = settings.aws_secret_access_key
        self.region = settings.aws_default_region
        if not self.key or not self.secret or not self.region:
            raise KeyError("Required AWS environment variables not found")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret,
            region_name=self.region,
        )
        """  you could use boto3.Session with a just a profile
        
        session = boto3.Session(profile_name="dev")
        # Any clients created from this session will use credentials
        # from the [dev] section of ~/.aws/credentials.
        self.s3 = session.client("s3")
        """

    def upload_file(
        self,
        file_path: str,
        bucket: str,
        extension: Optional[str] = None,
    ):
        if not extension:
            extension = file_path.split(".")[-1]
        try:
            self.s3.upload_file(
                file_path,
                bucket,
                basename(file_path),
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": f"image/{extension}",
                },
            )
            return f"https://{bucket}.s3.amazonaws.com/{basename(file_path)}"
        except ClientError as ex:
            logging.error(ex)
            raise HTTPException(400, "There was an error uploading file to S3")

    def download_file(self, key: str):
        pass
