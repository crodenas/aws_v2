"""
Data models for AWS STS (Security Token Service).
Contains dataclasses for responses from STS API calls.
"""

from dataclasses import dataclass
from typing import Optional

from . import base


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

    credentials: "base.CredentialsObject"
    assumed_role_user: AssumedRoleUserObject
