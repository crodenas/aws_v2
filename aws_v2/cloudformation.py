"module"

from dataclasses import dataclass
from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("cloudformation")


# Data models
# pylint: disable=invalid-name
@dataclass
class StackSummary:
    "class"

    # Add more fields as needed
    StackId: str
    StackName: str


@dataclass
class StackDescription:
    "class"

    # Add more fields as needed
    StackId: str
    StackName: str


@dataclass
class CreateStackResponse:
    "class"

    StackId: str


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def create_stack(
    stack_name: str,
    template_url: str,
    parameters: List,
    capabilities: List,
    cloudformation_client: boto3.client = None,
) -> CreateStackResponse:
    "function"

    if cloudformation_client is None:
        cloudformation_client = client

    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=parameters,
        Capabilities=capabilities,
    )

    return CreateStackResponse(**response)


@pivot_exceptions
def describe_stacks(
    stack_name: str = None,
    cloudformation_client: boto3.client = None,
) -> List[StackDescription]:
    "function"

    if cloudformation_client is None:
        cloudformation_client = client

    results = []

    paginator = cloudformation_client.get_paginator("describe_stacks")
    for page in paginator.paginate(StackName=stack_name):
        for stack in page["Stacks"]:
            results.append(StackDescription(**stack))

    return results


@pivot_exceptions
def list_stacks(
    stack_status_filter: str = None,
    cloudformation_client: boto3.client = None,
) -> List[StackSummary]:
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
            results.append(StackSummary(**summary))

    return results
