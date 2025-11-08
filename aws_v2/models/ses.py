"""
Data models for AWS SES (Simple Email Service).
Contains dataclasses for email messages and responses.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Email:
    """
    Represents the data required to send an email.

    Attributes:
        source: The email address of the sender.
        destination: The destination details, including To, Cc, and Bcc
            addresses.
        message: The content of the email, including Subject, Body,
            etc.
    """

    source: str
    destination: Dict
    message: Dict


@dataclass
class EmailResponse:
    """
    Represents the response from sending a standard email.

    Attributes:
        message_id: The unique identifier for the sent email.
        response_metadata: Metadata about the response, including HTTP
            status, request ID, etc.
    """

    message_id: str
    response_metadata: Dict


@dataclass
class RawEmailResponse:
    """
    Represents the response from sending a raw email.

    Attributes:
        message_id: The unique identifier for the sent raw email.
        response_metadata: Metadata about the response, including HTTP
            status, request ID, etc.
    """

    message_id: str
    response_metadata: Dict
