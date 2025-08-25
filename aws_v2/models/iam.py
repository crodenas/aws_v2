"""
Data models for AWS IAM (Identity and Access Management).
Contains dataclasses for IAM users, groups, roles, and policies.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Group:
    """
    Represents an IAM group.
    """

    group_name: str
    group_id: str


@dataclass
class User:
    """
    Represents an IAM user.
    """

    user_name: str
    user_id: str


@dataclass
class Role:
    """
    Represents an IAM role.
    """

    role_name: str
    role_id: str


@dataclass
class PolicyEntities:
    """
    Represents entities (users, groups, roles) associated with an IAM policy.
    """

    policy_groups: List[Group]
    policy_users: List[User]
    policy_roles: List[Role]
