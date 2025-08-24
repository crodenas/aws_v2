"module"

from dataclasses import dataclass
from datetime import datetime
from typing import List

import boto3
from botocore.response import StreamingBody

from . import session
from .exceptions import pivot_exceptions

client = session.client("s3")


# Data models
# pylint: disable=invalid-name
@dataclass
class Bucket:
    "class"

    Name: str
    CreationDate: datetime


@dataclass
class S3Object:
    "class"

    # Required fields
    Body: StreamingBody

    # Optional fields with defaults
    ContentType: str = None
    ContentLength: int = None
    LastModified: datetime = None
    ETag: str = None


@dataclass
class S3ObjectMetadata:
    "class"

    # Add more fields as needed
    Key: str


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def get_object(
    bucket_name: str, key: str, s3_client: boto3.client = client
) -> S3Object:
    "function"
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    # Create S3Object with the Body and pass other fields as keyword arguments
    return S3Object(
        Body=response["Body"],
        ContentType=response.get("ContentType"),
        ContentLength=response.get("ContentLength"),
        LastModified=response.get("LastModified"),
        ETag=response.get("ETag"),
    )


@pivot_exceptions
def list_buckets(s3_client: boto3.client = client) -> List[Bucket]:
    "function"
    pager = s3_client.get_paginator("list_buckets")
    response = pager.paginate()
    buckets = []
    for page in response:
        for bucket in page["Buckets"]:
            buckets.append(Bucket(**bucket))
    return buckets


@pivot_exceptions
def list_bucket_contents(
    bucket_name: str, s3_client: boto3.client = client
) -> List[S3ObjectMetadata]:
    "function"
    pager = s3_client.get_paginator("list_objects_v2")
    response = pager.paginate(Bucket=bucket_name)
    object_list = []
    for page in response:
        for list_item in page["Contents"]:
            object_list.append(S3ObjectMetadata(**list_item))
    return object_list
