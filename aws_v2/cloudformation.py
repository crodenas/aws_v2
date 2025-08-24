"module"

from dataclasses import dataclass
from typing import List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("cloudformation")


# Data models
# pylint: disable=invalid-name
@dataclass
class StackResponse:
    """Unified data model for stack responses."""

    StackId: Optional[str] = None
    StackName: Optional[str] = None
    # Add more optional fields as needed


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def create_stack(
    stack_name: str,
    template_url: str,
    parameters: List,
    capabilities: List,
    cloudformation_client: boto3.client = None,
) -> StackResponse:
    "function"

    if cloudformation_client is None:
        cloudformation_client = client

    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=parameters,
        Capabilities=capabilities,
    )

    return StackResponse(StackId=response["StackId"])


@pivot_exceptions
def describe_stacks(
    stack_name: str = None,
    cloudformation_client: boto3.client = None,
) -> List[StackResponse]:
    "function"

    if cloudformation_client is None:
        cloudformation_client = client

    results = []

    paginator = cloudformation_client.get_paginator("describe_stacks")
    for page in paginator.paginate(StackName=stack_name):
        for stack in page["Stacks"]:
            results.append(
                StackResponse(
                    StackId=stack.get("StackId"), StackName=stack.get("StackName")
                )
            )

    return results


@pivot_exceptions
def list_stacks(
    stack_status_filter: str = None,
    cloudformation_client: boto3.client = None,
) -> List[StackResponse]:
    "function"

    if cloudformation_client is None:
        cloudformation_client = client

    results = []

    params = {}
    if stack_status_filter:
        params["StackStatusFilter"] = stack_status_filter

    paginator = cloudformation_client.get_paginator("list_stacks")
    for page in paginator.paginate(**params):
        for summary in page["StackSummaries"]:
            results.append(
                StackResponse(
                    StackId=summary.get("StackId"), StackName=summary.get("StackName")
                )
            )

    return results
