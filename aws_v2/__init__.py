"module"

import boto3

from .models.base import CredentialsObject

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
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        aws_session_token=credentials.session_token,
        region_name=region_name,
    )
