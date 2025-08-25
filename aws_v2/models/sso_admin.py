"""
Data models for AWS SSO Admin service.
Contains dataclasses for SSO Admin operations.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AccountAssignmentCreationStatus:
    """
    Represents the status of an account assignment creation operation.
    """

    status: str
    request_id: str
    created_date: str
    failure_reason: Optional[str] = None
