"""EC2 utility functions for AWS operations."""

from dataclasses import dataclass
from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("ec2")


# Data models
# pylint: disable=invalid-name
@dataclass
class SecurityGroup:
    """Represents an AWS EC2 security group."""

    GroupId: str
    GroupName: str
    Description: str
    VpcId: str


# pylint: enable=invalid-name
# End Data models


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
                    GroupId=sg.get("GroupId", ""),
                    GroupName=sg.get("GroupName", ""),
                    Description=sg.get("Description", ""),
                    VpcId=sg.get("VpcId", ""),
                )
            )
    return results
