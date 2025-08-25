"""
Data models for AWS EC2 (Elastic Compute Cloud).
Contains dataclasses for EC2 resources like instances and security groups.
"""

from dataclasses import dataclass


@dataclass
class SecurityGroup:
    """
    Represents an AWS EC2 security group.
    """

    group_id: str
    group_name: str
    description: str
    vpc_id: str
