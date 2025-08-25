"""
This module provides utilities for interacting with AWS STS (Security Token Service).
Includes functions and data classes for assuming roles and retrieving caller identity.
"""

from dataclasses import dataclass
from typing import Optional

import boto3

from . import CredentialsObject, session
from .exceptions import pivot_exceptions

client = session.client("sts")


@dataclass
class CallerIdentityResponse:
    """
    Represents the response from get_caller_identity.
    Contains AWS account, user ID, and ARN.
    """

    account: str
    user_id: str
    arn: str


@dataclass
class AssumedRoleUserObject:
    """
    Represents the assumed role user object returned by STS.
    Contains the assumed role ID and ARN.
    """

    assumed_role_id: str
    arn: str


@dataclass
class AssumeRoleResponse:
    """
    Represents the response from assume_role.
    Contains credentials and assumed role user information.
    """

    credentials: CredentialsObject
    assumed_role_user: AssumedRoleUserObject


@pivot_exceptions
def assume_role(
    role_arn: str, region_name: str = None, sts_client: boto3.client = None
) -> AssumeRoleResponse:
    """
    Assumes an AWS IAM role and returns temporary credentials and role user info.

    Args:
        role_arn (str): The ARN of the role to assume.
        region_name (str, optional): AWS region name. Defaults to None.
        sts_client (boto3.client, optional): Custom STS client. Defaults to None.

    Returns:
        AssumeRoleResponse: Object containing credentials and assumed role user info.
    """
    if sts_client is None:
        sts_client = client
    if region_name is None:
        region_name = sts_client.meta.region_name

    response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="pivot-session")

    return AssumeRoleResponse(
        credentials=CredentialsObject(**response["Credentials"]),
        assumed_role_user=AssumedRoleUserObject(
            assumed_role_id=response["AssumedRoleUser"].get("AssumedRoleId"),
            arn=response["AssumedRoleUser"].get("Arn"),
        ),
    )


@pivot_exceptions
def get_caller_identity(
    sts_client: Optional[boto3.client] = None,
) -> CallerIdentityResponse:
    """
    Returns the AWS account, user ID, and ARN for the current credentials.

    Args:
        sts_client (boto3.client, optional): Custom STS client. Defaults to None.

    Returns:
        CallerIdentityResponse: Object containing account, user ID, and ARN.
    """
    if sts_client is None:
        sts_client = client
    response = sts_client.get_caller_identity()
    return CallerIdentityResponse(
        account=response["Account"], user_id=response["UserId"], arn=response["Arn"]
    )
