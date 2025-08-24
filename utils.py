"module"
import boto3
from botocore import waiter

from . import get_session, sts


def assume_role(role_arn: str, region_name: str = None) -> boto3.session.Session:
    "function"
    if region_name is None:
        region_name = sts.session.region_name

    assume_role_response = sts.assume_role(role_arn=role_arn)
    return get_session(assume_role_response.Credentials, region_name=region_name)


def get_client_with_role(
    service_name: str, role_arn: str, region_name: str = None
) -> boto3.client:
    "function"
    session = assume_role(role_arn=role_arn, region_name=region_name)
    return session.client(service_name)


def create_waiter(
    waiter_name: str, waiter_config: dict, client: boto3.client = None,
) -> waiter.Waiter:
    "function"
    waiter_model = waiter.WaiterModel(waiter_config)
    return waiter.create_waiter_with_client(
        waiter_name, waiter_model, client
    )