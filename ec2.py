"module"

from typing import Dict, List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("ec2")


@pivot_exceptions
def describe_security_groups(
    ec2_client: boto3.client = client,
) -> List[Dict]:
    "function"
    results = []

    paginator = ec2_client.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        results.extend(page["SecurityGroups"])

    return results
