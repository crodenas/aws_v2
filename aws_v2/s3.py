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

    # Add more fields as needed
    Body: StreamingBody

    def __init__(self, **kwargs):
        "function"
        self.Body = kwargs.get("Body")
        # You can add more fields here as needed
        # Example: self.ContentLength = kwargs.get("ContentLength")


@dataclass
class S3ObjectMetadata:
    "class"

    # Add more fields as needed
    Key: str

    def __init__(self, **kwargs):
        "function"
        self.Key = kwargs["Key"]


# pylint: enable=invalid-name
# End Data models


@pivot_exceptions
def get_object(
    bucket_name: str, key: str, s3_client: boto3.client = client
) -> S3Object:
    "function"
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return S3Object(**response)


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
