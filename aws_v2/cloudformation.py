"module"

from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.cloudformation import StackResponse

client = session.client("cloudformation")


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

    return StackResponse(
        stack_id=response["StackId"],
        stack_name=response["StackName"],
    )


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
                    stack_id=stack.get("StackId"),
                    stack_name=stack.get("StackName"),
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
                    stack_id=summary.get("StackId"),
                    stack_name=summary.get("StackName"),
                )
            )

    return results
