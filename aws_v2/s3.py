"module"

from dataclasses import dataclass
from datetime import datetime
from typing import List

import boto3
from botocore.response import StreamingBody

from . import session
from .exceptions import pivot_exceptions

client = session.client("s3")


@dataclass
class Bucket:
    "class"

    name: str
    creation_date: datetime


@dataclass
class S3Object:
    "class"

    # Required fields
    body: StreamingBody

    # Optional fields with defaults
    content_type: str = None
    content_length: int = None
    last_modified: datetime = None
    etag: str = None


@dataclass
class S3ObjectMetadata:
    "class"

    # Add more fields as needed
    key: str


@pivot_exceptions
def get_object(bucket_name: str, key: str, s3_client: boto3.client = None) -> S3Object:
    "function"
    if s3_client is None:
        s3_client = client
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    # Create S3Object with the Body and pass other fields as keyword arguments
    return S3Object(
        body=response["Body"],
        content_type=response.get("ContentType"),
        content_length=response.get("ContentLength"),
        last_modified=response.get("LastModified"),
        etag=response.get("ETag"),
    )


@pivot_exceptions
def list_buckets(s3_client: boto3.client = None) -> List[Bucket]:
    "function"
    if s3_client is None:
        s3_client = client
    pager = s3_client.get_paginator("list_buckets")
    response = pager.paginate()
    buckets = []
    for page in response:
        for bucket in page["Buckets"]:
            buckets.append(Bucket(bucket["Name"], bucket["CreationDate"]))
    return buckets


@pivot_exceptions
def list_bucket_contents(
    bucket_name: str, s3_client: boto3.client = None
) -> List[S3ObjectMetadata]:
    "function"
    if s3_client is None:
        s3_client = client
    pager = s3_client.get_paginator("list_objects_v2")
    response = pager.paginate(Bucket=bucket_name)
    object_list = []
    for page in response:
        for list_item in page["Contents"]:
            object_list.append(S3ObjectMetadata(key=list_item["Key"]))
    return object_list
