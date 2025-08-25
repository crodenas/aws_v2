"module"

from dataclasses import dataclass
from typing import Optional

import boto3

from . import CredentialsObject, session
from .exceptions import pivot_exceptions

client = session.client("sts")


@dataclass
class CallerIdentityResponse:
    "Represents the response from get_caller_identity."

    account: str
    user_id: str
    arn: str


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
def get_caller_identity(
    sts_client: Optional[boto3.client] = None,
) -> CallerIdentityResponse:
    "Returns the AWS account, user ID, and ARN for the current credentials."
    if sts_client is None:
        sts_client = client
    response = sts_client.get_caller_identity()
    return CallerIdentityResponse(
        account=response["Account"], user_id=response["UserId"], arn=response["Arn"]
    )
