"""
Utility functions for AWS role assumption and client creation.

This module provides helper functions for assuming IAM roles and creating
boto3 clients with assumed role credentials, as well as custom waiter
creation.
"""

from typing import Optional

import boto3
from botocore import waiter

from . import get_session, sts


def assume_role(
    role_arn: str, region_name: Optional[str] = None
) -> boto3.session.Session:
    """
    Assume an IAM role and return a boto3 session with the credentials.

    Args:
        role_arn: The ARN of the role to assume.
        region_name: AWS region name. If None, uses the default session
            region.

    Returns:
        A boto3 session configured with the assumed role credentials.
    """
    if region_name is None:
        region_name = sts.session.region_name

    assume_role_response = sts.assume_role(role_arn=role_arn)
    return get_session(
        assume_role_response.credentials, region_name=region_name
    )


def get_client_with_role(
    service_name: str,
    role_arn: str,
    region_name: Optional[str] = None,
) -> boto3.client:
    """
    Create a boto3 client with assumed role credentials.

    Args:
        service_name: Name of the AWS service (e.g., 's3', 'ec2').
        role_arn: The ARN of the role to assume.
        region_name: AWS region name. If None, uses the default session
            region.

    Returns:
        A boto3 client for the specified service using assumed role
        credentials.
    """
    session = assume_role(role_arn=role_arn, region_name=region_name)
    return session.client(service_name)


def create_waiter(
    waiter_name: str,
    waiter_config: dict,
    client: Optional[boto3.client] = None,
) -> waiter.Waiter:
    """
    Create a custom waiter with the specified configuration.

    Args:
        waiter_name: Name for the custom waiter.
        waiter_config: Dictionary containing the waiter configuration.
        client: boto3 client to use with the waiter. Defaults to None.

    Returns:
        A configured waiter object.
    """
    waiter_model = waiter.WaiterModel(waiter_config)
    return waiter.create_waiter_with_client(
        waiter_name, waiter_model, client
    )
