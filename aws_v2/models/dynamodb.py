"""
Data models for DynamoDB operations.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class DynamoDBScanOutput:
    """
    Represents the output of a DynamoDB scan operation.
    """

    items: List[Dict]
    count: int
    scanned_count: int
    last_evaluated_key: Optional[Dict] = None
    consumed_capacity: Optional[Dict] = None
