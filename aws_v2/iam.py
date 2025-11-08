"""
AWS IAM service module.

This module provides functions for interacting with AWS IAM (Identity and
Access Management), including operations for listing entities attached to
policies.
"""

from typing import Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.iam import Group, PolicyEntities, Role, User

client = session.client("iam")


@pivot_exceptions
def list_entities_for_policy(
    policy_arn: str,
    entity_filter: Optional[str] = None,
    path_prefix: Optional[str] = None,
    policy_usage_filter: Optional[str] = None,
    iam_client: Optional[boto3.client] = None,
) -> PolicyEntities:
    """
    List all IAM entities (users, groups, roles) attached to a policy.

    Args:
        policy_arn: The ARN of the policy to query.
        entity_filter: Filter results by entity type. Defaults to None.
        path_prefix: Filter results by path prefix. Defaults to None.
        policy_usage_filter: Filter by policy usage. Defaults to None.
        iam_client: Custom IAM client. Defaults to module client.

    Returns:
        PolicyEntities object containing lists of groups, users, and
        roles attached to the policy.
    """
    if iam_client is None:
        iam_client = client

    results = {}

    params = {
        "PolicyArn": policy_arn,
    }
    if entity_filter is not None:
        params["EntityFilter"] = entity_filter
    if path_prefix is not None:
        params["PathPrefix"] = path_prefix
    if policy_usage_filter is not None:
        params["PolicyUsageFilter"] = policy_usage_filter

    paginator = iam_client.get_paginator("list_entities_for_policy")
    for page in paginator.paginate(**params):
        results.update(page)

    return PolicyEntities(
        policy_groups=[
            Group(group_name=group["GroupName"], group_id=group["GroupId"])
            for group in results.get("PolicyGroups", [])
        ],
        policy_users=[
            User(user_name=user["UserName"], user_id=user["UserId"])
            for user in results.get("PolicyUsers", [])
        ],
        policy_roles=[
            Role(role_name=role["RoleName"], role_id=role["RoleId"])
            for role in results.get("PolicyRoles", [])
        ],
    )
