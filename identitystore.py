"module"

from typing import Dict, List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("identitystore")


@pivot_exceptions
def list_groups(
    identitystore_id: str, identitystore_client: boto3.client = client
) -> List[Dict[str, str]]:
    "function"
    results = []

    paginator = identitystore_client.get_paginator("list_groups")
    for page in paginator.paginate(IdentityStoreId=identitystore_id):
        results.extend(page["Groups"])

    return results
