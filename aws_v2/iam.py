"module"

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.iam import Group, PolicyEntities, Role, User

client = session.client("iam")


@pivot_exceptions
def list_entities_for_policy(
    policy_arn: str,
    entity_filter: str = None,
    path_prefix: str = None,
    policy_usage_filter: str = None,
    iam_client: boto3.client = None,
) -> PolicyEntities:
    "function"
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
