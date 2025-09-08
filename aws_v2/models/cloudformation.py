"""
Data models for AWS CloudFormation.
Contains dataclasses for CloudFormation stacks and related resources.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class StackResponse:
    """
    Unified data model for CloudFormation stack responses.
    Can be extended with more fields as needed.
    """

    description: Optional[str] = None
    outputs: Optional[List[Dict[str, str]]] = None
    parameters: Optional[List[Dict[str, str]]] = None
    stack_id: Optional[str] = None
    stack_name: Optional[str] = None
