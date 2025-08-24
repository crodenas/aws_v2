"""EC2 utility functions for AWS operations."""

from dataclasses import dataclass
from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("ec2")


@dataclass
class SecurityGroup:
    """Represents an AWS EC2 security group."""

    group_id: str
    group_name: str
    description: str
    vpc_id: str


@pivot_exceptions
def describe_security_groups(ec2_client: boto3.client = None) -> List[SecurityGroup]:
    """Retrieve all EC2 security groups using pagination."""
    if ec2_client is None:
        ec2_client = client
    results = []
    paginator = ec2_client.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for sg in page["SecurityGroups"]:
            results.append(
                SecurityGroup(
                    group_id=sg.get("GroupId", ""),
                    group_name=sg.get("GroupName", ""),
                    description=sg.get("Description", ""),
                    vpc_id=sg.get("VpcId", ""),
                )
            )
    return results
