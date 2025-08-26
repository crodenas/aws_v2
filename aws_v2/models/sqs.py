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
