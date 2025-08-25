"""Organizations models module."""

from dataclasses import dataclass
from datetime import datetime


from .base import BaseModel


@dataclass
class Account(BaseModel):
    """AWS Account model representing an account in an AWS Organization."""

    id: str
    arn: str
    email: str
    name: str
    status: str
    joined_method: str
    joined_timestamp: datetime


# Tag dataclass for resource tagging
@dataclass
class Tag:
    key: str
    value: str
