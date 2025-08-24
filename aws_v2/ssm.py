"""
AWS Systems Manager (SSM) Parameter Store operations.

This module provides functions for interacting with AWS Systems Manager Parameter Store,
including retrieving, creating, updating, and deleting parameters. It handles AWS API pagination
and provides consistent error handling through the pivot_exceptions decorator.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import boto3
from botocore.config import Config

from . import session
from .exceptions import pivot_exceptions

# Maximum retry attempts for AWS SSM client operations. This value was chosen based on AWS SDK's
# recommendation for standard retry mode, balancing reliability and performance.
MAX_RETRY_ATTEMPTS = 10

config = Config(
    retries={
        "max_attempts": MAX_RETRY_ATTEMPTS,
        "mode": "standard",
    },
)
client = session.client("ssm", config=config)


@dataclass
class Parameter:
    """Represents an SSM Parameter with its attributes

    Attributes:
        name: The name/key of the parameter
        value: The value of the parameter
        last_modified_date: When the parameter was last modified (optional)
    """

    name: str
    value: str
    last_modified_date: datetime = None

    def to_dict(self):
        """Convert Parameter to a dictionary for JSON serialization"""
        result = {
            "Name": self.name,
            "Value": self.value,
        }
        if self.last_modified_date:
            result["LastModifiedDate"] = self.last_modified_date.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        return result


@pivot_exceptions
def delete_parameter(name: str, ssm_client: boto3.client = None) -> None:
    """Delete a parameter from SSM Parameter Store

    Args:
        name: Name of the parameter to delete
        ssm_client: Optional boto3 SSM client to use
    """
    if ssm_client is None:
        ssm_client = client
    ssm_client.delete_parameter(Name=name)


@pivot_exceptions
def get_parameter(
    name: str, decrypt: bool = True, ssm_client: boto3.client = None
) -> Parameter:
    """Retrieve a parameter from SSM Parameter Store

    Args:
        name: Name of the parameter to retrieve
        decrypt: Whether to decrypt SecureString parameters (default: True)
        ssm_client: Optional boto3 SSM client to use

    Returns:
        Parameter: A Parameter object containing the requested parameter data
    """
    if ssm_client is None:
        ssm_client = client
    response = ssm_client.get_parameter(Name=name, WithDecryption=decrypt)
    parameter = response["Parameter"]

    return Parameter(
        name=parameter["Name"],
        value=parameter["Value"],
        last_modified_date=parameter["LastModifiedDate"],
    )


@pivot_exceptions
def get_parameters_by_path(
    path: str, decrypt: bool = True, ssm_client: boto3.client = None
) -> List[Parameter]:
    """Retrieve all parameters under a specific path hierarchy from SSM Parameter Store

    Args:
        path: The hierarchy path to retrieve parameters from
        decrypt: Whether to decrypt SecureString parameters (default: True)
        ssm_client: Optional boto3 SSM client to use

    Returns:
        List[Parameter]: A list of Parameter objects matching the path
    """
    results = []

    if ssm_client is None:
        ssm_client = client

    paginator = ssm_client.get_paginator("get_parameters_by_path")
    for page in paginator.paginate(Path=path, WithDecryption=decrypt):
        for parameter in page["Parameters"]:
            results.append(
                Parameter(
                    name=parameter["Name"],
                    value=parameter["Value"],
                    last_modified_date=parameter["LastModifiedDate"],
                )
            )

    return results


@pivot_exceptions
def put_parameter(
    parameter: Parameter,
    overwrite: bool = True,
    param_type: str = "SecureString",
    ssm_client: boto3.client = None,
) -> None:
    """Store a parameter in SSM Parameter Store

    Args:
        parameter: Parameter object to store
        overwrite: Whether to overwrite existing parameter (default: True)
        param_type: Parameter type, one of 'String', 'StringList', or 'SecureString' (default: 'SecureString')
        ssm_client: Optional boto3 SSM client to use
    """
    if ssm_client is None:
        ssm_client = client
    ssm_client.put_parameter(
        Name=parameter.name,
        Value=parameter.value,
        Overwrite=overwrite,
        Type=param_type,
    )
