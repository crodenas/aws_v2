"""
AWS v2 SDK Wrapper initialization module.

This module provides the global boto3 session and utility functions for
creating AWS service clients and sessions with custom credentials.
"""

import boto3

from .models.base import CredentialsObject

session: boto3.session.Session = boto3.session.Session()
if session.region_name is None:
    session = boto3.session.Session(region_name="us-east-2")


def get_client(
    service_name: str,
    region_name: str,
    boto3_session: boto3.session.Session = session,
) -> boto3.client:
    """
    Create a boto3 client for the specified AWS service.

    Args:
        service_name: Name of the AWS service (e.g., 's3', 'ec2').
        region_name: AWS region name for the client.
        boto3_session: The boto3 session to use. Defaults to module
            session.

    Returns:
        A boto3 client for the specified service and region.
    """
    return boto3_session.client(service_name, region_name=region_name)


def get_session(
    credentials: CredentialsObject, region_name: str
) -> boto3.session.Session:
    """
    Create a new boto3 session with the provided credentials.

    Args:
        credentials: AWS credentials object containing access keys and
            session token.
        region_name: AWS region name for the session.

    Returns:
        A new boto3 session configured with the provided credentials.
    """
    return boto3.session.Session(
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        aws_session_token=credentials.session_token,
        region_name=region_name,
    )
