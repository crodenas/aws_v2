"""
Base data models for AWS SDK wrapper.
Contains common dataclasses used across multiple AWS services.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CredentialsObject:
    """
    Represents AWS credentials including access keys and session token.
    """

    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime
