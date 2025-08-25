"""
Data models for AWS S3 (Simple Storage Service).
Contains dataclasses for S3 buckets and objects.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from botocore.response import StreamingBody


@dataclass
class Bucket:
    """
    Represents an S3 bucket.
    """

    name: str
    creation_date: datetime


@dataclass
class S3Object:
    """
    Represents an S3 object with its metadata and content.
    """

    # Required fields
    body: StreamingBody

    # Optional fields with defaults
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None


@dataclass
class S3ObjectMetadata:
    """
    Represents metadata about an S3 object.
    """

    key: str
