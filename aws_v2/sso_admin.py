"""
This module provides functionality for interacting with the AWS SSO Admin service.
It includes methods for creating account assignments and handling exceptions.
"""

from dataclasses import dataclass

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("sso-admin")


@dataclass
class AccountAssignmentCreationStatus:
    """
    Represents the status of an account assignment creation operation.
    """

    status: str
    request_id: str
    created_date: str
    failure_reason: str = None


@pivot_exceptions
def create_account_assignment(
    instance_arn: str,
    permission_set_arn: str,
    principal_id: str,
    target_id: str,
    principal_type: str,
    sso_admin_client: boto3.client = None,
) -> AccountAssignmentCreationStatus:
    """
    Create an account assignment in AWS SSO.

    Args:
        instance_arn (str): The ARN of the SSO instance.
        permission_set_arn (str): The ARN of the permission set.
        principal_id (str): The ID of the principal (user or group).
        target_id (str): The ID of the target AWS account.
        principal_type (str): The type of the principal (e.g., USER or GROUP).
        sso_admin_client (boto3.client, optional): A boto3 SSO Admin client. Defaults to None.

    Returns:
        AccountAssignmentCreationStatus: An instance of AccountAssignmentCreationStatus containing
            the details of the account assignment.
    """
    if sso_admin_client is None:
        sso_admin_client = client

    response = sso_admin_client.create_account_assignment(
        InstanceArn=instance_arn,
        PermissionSetArn=permission_set_arn,
        PrincipalId=principal_id,
        PrincipalType=principal_type,
        TargetId=target_id,
        TargetType="AWS_ACCOUNT",
    )

    return AccountAssignmentCreationStatus(
        status=response.get("AccountAssignment").get("Status"),
        request_id=response.get("AccountAssignment").get("RequestId"),
        created_date=response.get("AccountAssignment").get("CreatedDate"),
        failure_reason=response.get("AccountAssignment").get("FailureReason"),
    )
