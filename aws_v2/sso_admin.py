"module"

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("sso-admin")


@pivot_exceptions
def create_account_assignment(
    instance_arn: str,
    permission_set_arn: str,
    principal_id: str,
    target_id: str,
    principal_type: str,
    sso_admin_client: boto3.client = None,
) -> str:
    "function"
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

    return response["RequestId"]
