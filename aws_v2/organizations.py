"""
AWS Organizations service module.

This module provides functions for interacting with AWS Organizations,
including operations for describing accounts, listing accounts, and
managing resource tags.
"""

from typing import List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.organizations import Account, Tag

client = session.client("organizations")


@pivot_exceptions
def describe_account(
    account_id: str, organizations_client: Optional[boto3.client] = None
) -> Account:
    """
    Describe an AWS account by its ID.

    Args:
        account_id: The AWS account ID to describe.
        organizations_client: Custom Organizations client. Defaults to
            module client.

    Returns:
        An Account object containing account details.
    """
    if organizations_client is None:
        organizations_client = client

    response = organizations_client.describe_account(AccountId=account_id)
    acct = response.get("Account", {})
    return Account(
        id=acct["Id"],
        arn=acct["Arn"],
        email=acct["Email"],
        name=acct["Name"],
        status=acct["Status"],
        joined_method=acct["JoinedMethod"],
        joined_timestamp=acct["JoinedTimestamp"],
    )


@pivot_exceptions
def list_accounts(
    organizations_client: Optional[boto3.client] = None,
) -> List[Account]:
    """
    List all AWS accounts using pagination.

    Args:
        organizations_client: Custom Organizations client. Defaults to
            module client.

    Returns:
        A list of Account objects for all accounts in the organization.
    """
    if organizations_client is None:
        organizations_client = client

    results = []
    paginator = organizations_client.get_paginator("list_accounts")
    for page in paginator.paginate():
        accounts = page.get("Accounts", [])
        results.extend(
            Account(
                id=acct["Id"],
                arn=acct["Arn"],
                email=acct["Email"],
                name=acct["Name"],
                status=acct["Status"],
                joined_method=acct["JoinedMethod"],
                joined_timestamp=acct["JoinedTimestamp"],
            )
            for acct in accounts
        )

    return results


@pivot_exceptions
def list_tags_for_resource(
    resource_arn: str, organizations_client: Optional[boto3.client] = None
) -> List[Tag]:
    """
    List all tags for a given resource.

    Args:
        resource_arn: The ARN of the resource to list tags for.
        organizations_client: Custom Organizations client. Defaults to
            module client.

    Returns:
        A list of Tag objects containing key-value pairs.
    """
    if organizations_client is None:
        organizations_client = client

    response = organizations_client.list_tags_for_resource(
        ResourceARN=resource_arn
    )
    tags = response.get("Tags", [])
    return [Tag(key=tag["Key"], value=tag["Value"]) for tag in tags]
