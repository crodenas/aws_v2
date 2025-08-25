"""
Data models for AWS CloudFormation.
Contains dataclasses for CloudFormation stacks and related resources.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StackResponse:
    """
    Unified data model for CloudFormation stack responses.
    Can be extended with more fields as needed.
    """

    stack_id: Optional[str] = None
    stack_name: Optional[str] = None
