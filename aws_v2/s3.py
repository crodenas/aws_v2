"""
AWS S3 service module.

This module provides functions for interacting with AWS S3, including
operations for retrieving objects, listing buckets, and listing bucket
contents.
"""

from typing import List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.s3 import Bucket, S3Object, S3ObjectMetadata

client = session.client("s3")


@pivot_exceptions
def get_object(
    bucket_name: str,
    key: str,
    s3_client: Optional[boto3.client] = None,
) -> S3Object:
    """
    Retrieve an object from an S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        key: The key (path) of the object within the bucket.
        s3_client: Custom S3 client. Defaults to module client.

    Returns:
        An S3Object containing the object's body and metadata.
    """
    if s3_client is None:
        s3_client = client
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    # Create S3Object with the Body and pass other fields as keyword
    # arguments
    return S3Object(
        body=response["Body"],
        content_type=response.get("ContentType"),
        content_length=response.get("ContentLength"),
        last_modified=response.get("LastModified"),
        etag=response.get("ETag"),
    )


@pivot_exceptions
def list_buckets(
    s3_client: Optional[boto3.client] = None,
) -> List[Bucket]:
    """
    List all S3 buckets in the account.

    Args:
        s3_client: Custom S3 client. Defaults to module client.

    Returns:
        A list of Bucket objects containing bucket names and creation
        dates.
    """
    if s3_client is None:
        s3_client = client

    pager = s3_client.get_paginator("list_buckets")
    response = pager.paginate()

    result = []
    for page in response:
        for bucket in page["Buckets"]:
            result.append(
                Bucket(
                    name=bucket["Name"],
                    creation_date=bucket["CreationDate"],
                )
            )
    return result


@pivot_exceptions
def list_bucket_contents(
    bucket_name: str, s3_client: Optional[boto3.client] = None
) -> List[S3ObjectMetadata]:
    """
    List all objects in an S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        s3_client: Custom S3 client. Defaults to module client.

    Returns:
        A list of S3ObjectMetadata objects containing object keys.
    """
    if s3_client is None:
        s3_client = client
    pager = s3_client.get_paginator("list_objects_v2")
    response = pager.paginate(Bucket=bucket_name)
    object_list = []
    for page in response:
        for list_item in page.get("Contents", []):
            object_list.append(S3ObjectMetadata(key=list_item["Key"]))
    return object_list
