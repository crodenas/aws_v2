"""
AWS CloudFormation service module.

This module provides functions for interacting with AWS CloudFormation,
including operations for creating stacks, describing stacks, and listing
stacks with various filters.
"""

from typing import Dict, List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.cloudformation import StackResponse

client = session.client("cloudformation")


@pivot_exceptions
def create_stack(
    stack_name: str,
    template_url: str,
    parameters: List[Dict[str, str]],
    capabilities: List[str],
    cloudformation_client: Optional[boto3.client] = None,
) -> StackResponse:
    """
    Create a new CloudFormation stack.

    Args:
        stack_name: The name for the new stack.
        template_url: The URL of the template to use for stack creation.
        parameters: A list of parameter dictionaries for the stack.
        capabilities: A list of capabilities required for the stack.
        cloudformation_client: Custom CloudFormation client. Defaults to
            module client.

    Returns:
        A StackResponse object containing the stack ID and name.
    """
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
        stack_name=stack_name,
    )


@pivot_exceptions
def describe_stacks(
    stack_name: Optional[str] = None,
    cloudformation_client: Optional[boto3.client] = None,
) -> List[StackResponse]:
    """
    Describe CloudFormation stacks.

    Args:
        stack_name: Optional name of a specific stack to describe.
            If None, describes all stacks.
        cloudformation_client: Custom CloudFormation client. Defaults to
            module client.

    Returns:
        A list of StackResponse objects containing stack details.
    """
    if cloudformation_client is None:
        cloudformation_client = client

    params = {}
    if stack_name:
        params["StackName"] = stack_name

    results = []
    paginator = cloudformation_client.get_paginator("describe_stacks")
    for page in paginator.paginate(**params):
        for stack in page["Stacks"]:
            results.append(
                StackResponse(
                    stack_id=stack.get("StackId"),
                    stack_name=stack.get("StackName"),
                    description=stack.get("Description"),
                    parameters=stack.get("Parameters"),
                    outputs=stack.get("Outputs"),
                )
            )

    return results


@pivot_exceptions
def list_stacks(
    stack_status_filter: Optional[str] = None,
    cloudformation_client: Optional[boto3.client] = None,
) -> List[StackResponse]:
    """
    List CloudFormation stacks with optional status filtering.

    Args:
        stack_status_filter: Optional status filter for stacks.
            Defaults to None.
        cloudformation_client: Custom CloudFormation client. Defaults to
            module client.

    Returns:
        A list of StackResponse objects containing stack summaries.
    """
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
