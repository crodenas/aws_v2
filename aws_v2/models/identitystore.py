"""
Data models for AWS Identity Store.
Contains dataclasses for Identity Store resources.
"""

from dataclasses import dataclass


@dataclass
class Group:
    """
    Represents a group in the AWS Identity Store.

    Attributes:
        group_id (str): The unique identifier of the group.
        display_name (str): The display name of the group.
    """

    group_id: str
    display_name: str
