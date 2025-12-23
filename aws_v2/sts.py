"""
This module provides utilities for interacting with AWS STS (Security
Token Service).

Includes functions for assuming roles and retrieving caller identity.
"""

from typing import Optional

import boto3

from . import CredentialsObject, session
from .exceptions import pivot_exceptions
from .models.sts import (
    AssumedRoleUserObject,
    AssumeRoleResponse,
    CallerIdentityResponse,
)

client = session.client("sts")


@pivot_exceptions
def assume_role(
    role_arn: str,
    sts_client: Optional[boto3.client] = None,
) -> AssumeRoleResponse:
    """
    Assumes an AWS IAM role and returns temporary credentials and role
    user info.

    Args:
        role_arn: The ARN of the role to assume.
        sts_client: Custom STS client. Defaults to None.

    Returns:
        Object containing credentials and assumed role user info.
    """
    if sts_client is None:
        sts_client = client

    response = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="pivot-session"
    )

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
    Returns the AWS account, user ID, and ARN for the current
    credentials.

    Args:
        sts_client: Custom STS client. Defaults to None.

    Returns:
        Object containing account, user ID, and ARN.
    """
    if sts_client is None:
        sts_client = client
    response = sts_client.get_caller_identity()
    return CallerIdentityResponse(
        account=response["Account"],
        user_id=response["UserId"],
        arn=response["Arn"],
    )
