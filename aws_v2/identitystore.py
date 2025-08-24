"""
This module provides functionality for interacting with AWS Identity Store.
It includes a dataclass for representing groups and a function for listing groups.
"""

from dataclasses import dataclass
from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("identitystore")


# Data models
# pylint: disable=invalid-name
@dataclass
class Group:
    """
    Represents a group in the AWS Identity Store.

    Attributes:
        GroupId (str): The unique identifier of the group.
        DisplayName (str): The display name of the group.
    """

    GroupId: str
    DisplayName: str


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def list_groups(
    identitystore_id: str, identitystore_client: boto3.client = client
) -> List[Group]:
    """
    Lists all groups in the specified AWS Identity Store.

    Args:
        identitystore_id (str): The ID of the AWS Identity Store.
        identitystore_client (boto3.client, optional): The boto3 client for
            Identity Store. Defaults to the module-level client.

    Returns:
        List[Group]: A list of Group objects representing the groups in the Identity Store.
    """
    results = []

    paginator = identitystore_client.get_paginator("list_groups")
    for page in paginator.paginate(IdentityStoreId=identitystore_id):
        results.extend(Group(**group) for group in page["Groups"])

    return results
