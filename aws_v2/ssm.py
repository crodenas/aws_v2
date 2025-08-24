"module"

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


# Data models
# pylint: disable=invalid-name
@dataclass
class Parameter:
    "class"

    Name: str
    Value: str
    LastModifiedDate: datetime = None

    def to_dict(self):
        """Convert Parameter to a dictionary for JSON serialization"""
        return {
            "Name": self.Name,
            "Value": self.Value,
            "LastModifiedDate": self.LastModifiedDate.strftime("%Y-%m-%dT%H:%M:%S"),
        }


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def delete_parameter(name: str, ssm_client: boto3.client = client) -> None:
    "function"
    ssm_client.delete_parameter(Name=name)


@pivot_exceptions
def get_parameter(name: str, ssm_client: boto3.client = client) -> Parameter:
    "function"
    decrypt = True

    response = ssm_client.get_parameter(Name=name, WithDecryption=decrypt)
    parameter = response["Parameter"]

    return Parameter(
        Name=parameter["Name"],
        Value=parameter["Value"],
        LastModifiedDate=parameter["LastModifiedDate"],
    )


@pivot_exceptions
def get_parameters_by_path(
    path: str, ssm_client: boto3.client = client
) -> List[Parameter]:
    "function"
    decrypt = True
    results = []

    paginator = ssm_client.get_paginator("get_parameters_by_path")
    for page in paginator.paginate(Path=path, WithDecryption=decrypt):
        for parameter in page["Parameters"]:
            results.append(
                Parameter(
                    Name=parameter["Name"],
                    Value=parameter["Value"],
                    LastModifiedDate=parameter["LastModifiedDate"],
                )
            )

    return results


@pivot_exceptions
def put_parameter(
    parameter: Parameter,
    ssm_client: boto3.client = client,
) -> None:
    "function"
    overwrite = True
    param_type = "SecureString"

    ssm_client.put_parameter(
        Name=parameter.Name,
        Value=parameter.Value,
        Overwrite=overwrite,
        Type=param_type,
    )
