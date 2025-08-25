"""
Data models for AWS SSM (Systems Manager).
Contains dataclasses for SSM parameters and related resources.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Parameter:
    """
    Represents an SSM Parameter with its attributes.

    Attributes:
        name: The name/key of the parameter
        value: The value of the parameter
        last_modified_date: When the parameter was last modified (optional)
    """

    name: str
    value: str
    last_modified_date: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert Parameter to a dictionary for JSON serialization."""
        result = {
            "Name": self.name,
            "Value": self.value,
        }
        if self.last_modified_date:
            result["LastModifiedDate"] = self.last_modified_date.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        return result
