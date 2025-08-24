"module"

from dataclasses import dataclass
from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("iam")


# Data models
# pylint: disable=invalid-name
@dataclass
class Group:
    "class"

    GroupName: str
    GroupId: str


@dataclass
class User:
    "class"

    UserName: str
    UserId: str


@dataclass
class Role:
    "class"

    RoleName: str
    RoleId: str


@dataclass
class PolicyEntities:
    "class"

    PolicyGroups: List[Group]
    PolicyUsers: List[User]
    PolicyRoles: List[Role]


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def list_entities_for_policy(
    policy_arn: str,
    entity_filter: str = None,
    path_prefix: str = None,
    policy_usage_filter: str = None,
    iam_client: boto3.client = client,
) -> PolicyEntities:
    "function"
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
        PolicyGroups=[Group(**group) for group in results.get("PolicyGroups", [])],
        PolicyUsers=[User(**user) for user in results.get("PolicyUsers", [])],
        PolicyRoles=[Role(**role) for role in results.get("PolicyRoles", [])],
    )
