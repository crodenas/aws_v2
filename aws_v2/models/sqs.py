"""
Models for AWS SQS (Simple Queue Service) operations.
"""

from dataclasses import dataclass


@dataclass
class SQSMessageResponse:
    """
    Represents the response of an SQS send_message operation.

    Attributes:
        message_id (str): The ID of the sent message.
        md5_of_message_body (str): The MD5 checksum of the message body.
    """

    message_id: str
    md5_of_message_body: str


@dataclass
class SQSMessage:
    """
    Represents an SQS message.

    Attributes:
        message_id (str): The ID of the message.
        receipt_handle (str): The receipt handle for the message.
        body (str): The body content of the message.
    """

    message_id: str
    receipt_handle: str
    body: str
