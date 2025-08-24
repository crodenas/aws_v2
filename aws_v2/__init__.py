"module"

import os
from dataclasses import dataclass
from datetime import datetime

import boto3


# Data models
# pylint: disable=invalid-name
@dataclass
class CredentialsObject:
    "class"

    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str
    Expiration: datetime


# pylint: enable=invalid-name
# End Data models

session: boto3.session.Session = boto3.session.Session()
if session.region_name is None:
    session = boto3.session.Session(region_name="us-east-2")


def get_client(
    service_name: str,
    region_name: str,
    boto3_session: boto3.session = session,
) -> boto3.client:
    "function"
    return boto3_session.client(service_name, region_name=region_name)


def get_session(
    credentials: CredentialsObject, region_name: str
) -> boto3.session.Session:
    "function"

    return boto3.session.Session(
        aws_access_key_id=credentials.AccessKeyId,
        aws_secret_access_key=credentials.SecretAccessKey,
        aws_session_token=credentials.SessionToken,
        region_name=region_name,
    )
