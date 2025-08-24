"module"

from dataclasses import dataclass

import boto3

from . import CredentialsObject, session
from .exceptions import pivot_exceptions

client = session.client("sts")


# Data models
# pylint: disable=invalid-name
@dataclass
class AssumedRoleUserObject:
    "class"

    AssumedRoleId: str
    Arn: str


@dataclass
class AssumeRoleResponse:
    "class"

    Credentials: CredentialsObject
    AssumedRoleUser: AssumedRoleUserObject

    def __init__(self, **kwargs):
        self.Credentials = CredentialsObject(**kwargs["Credentials"])
        self.AssumedRoleUser = AssumedRoleUserObject(**kwargs["AssumedRoleUser"])


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def assume_role(
    role_arn: str, region_name: str = None, sts_client: boto3.client = client
) -> AssumeRoleResponse:
    "function"
    if region_name is None:
        region_name = sts_client.meta.region_name

    assumed_role: AssumeRoleResponse = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession"
    )
    return AssumeRoleResponse(**assumed_role)


@pivot_exceptions
def get_caller_identity(sts_client: boto3.client = client):
    "function"
    return sts_client.get_caller_identity()
