"""
This module provides functionality for interacting with AWS Identity Store.
It includes functionality for listing groups.
"""

from typing import List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.identitystore import Group

client = session.client("identitystore")


@pivot_exceptions
def list_groups(
    identitystore_id: str,
    identitystore_client: Optional[boto3.client] = None,
) -> List[Group]:
    """
    Lists all groups in the specified AWS Identity Store.

    Args:
        identitystore_id: The ID of the AWS Identity Store.
        identitystore_client: The boto3 client for Identity Store.
            Defaults to the module-level client.

    Returns:
        A list of Group objects representing the groups in the Identity
        Store.
    """
    results = []

    if identitystore_client is None:
        identitystore_client = client

    paginator = identitystore_client.get_paginator("list_groups")
    for page in paginator.paginate(IdentityStoreId=identitystore_id):
        results.extend(
            Group(
                group_id=group["GroupId"],
                display_name=group["DisplayName"],
            )
            for group in page["Groups"]
        )

    return results
