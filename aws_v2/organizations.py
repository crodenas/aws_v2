"module"

from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.organizations import Account

client = session.client("organizations")


@pivot_exceptions
def list_accounts(organizations_client: boto3.client = None) -> List[Account]:
    """List all AWS accounts using pagination."""
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
def describe_account(
    account_id: str, organizations_client: boto3.client = None
) -> Account:
    """Describe an AWS account by its ID."""
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
