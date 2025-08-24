"""EC2 utility functions for AWS operations."""

from typing import List
from dataclasses import dataclass


@dataclass
class SecurityGroup:
    GroupId: str
    GroupName: str
    Description: str
    VpcId: str


import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("ec2")


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
