"module"

from dataclasses import dataclass

import boto3

from . import CredentialsObject, session
from .exceptions import pivot_exceptions

client = session.client("sts")


@dataclass
class AssumedRoleUserObject:
    "class"

    assumed_role_id: str
    arn: str


@dataclass
class AssumeRoleResponse:
    "class"

    credentials: CredentialsObject
    assumed_role_user: AssumedRoleUserObject


@pivot_exceptions
def assume_role(
    role_arn: str, region_name: str = None, sts_client: boto3.client = None
) -> AssumeRoleResponse:
    "function"
    if sts_client is None:
        sts_client = client
    if region_name is None:
        region_name = sts_client.meta.region_name

    response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="pivot-session")

    return AssumeRoleResponse(
        credentials=CredentialsObject(**response["Credentials"]),
        assumed_role_user=AssumedRoleUserObject(**response["AssumedRoleUser"]),
    )


@pivot_exceptions
def get_caller_identity(sts_client: boto3.client = None):
    "function"
    if sts_client is None:
        sts_client = client
    return sts_client.get_caller_identity()
