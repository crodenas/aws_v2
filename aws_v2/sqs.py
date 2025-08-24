"""
This module provides utilities for interacting with AWS SQS (Simple Queue Service).
It includes functions for extracting the region from an SQS URL and sending messages
    to an SQS queue.
"""

from dataclasses import dataclass

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("sqs")


def get_region_from_url(url: str) -> str:
    """
    Extract the AWS region from an SQS queue URL.

    Args:
        url (str): The SQS queue URL.

    Returns:
        str: The AWS region extracted from the URL.
    """
    return url.split(".")[1]


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


@pivot_exceptions
def send_message(
    queue_url: str, message_body: str, sqs_client: boto3.client = None
) -> SQSMessageResponse:
    """
    Send a message to an SQS queue.

    Args:
        queue_url (str): The URL of the SQS queue.
        message_body (str): The content of the message to send.
        sqs_client (boto3.client, optional): A custom SQS client. Defaults to the module's client.

    Returns:
        SQSMessageResponse: The response containing the message ID and MD5 checksum.
    """
    if sqs_client is None:
        sqs_client = client
    response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return SQSMessageResponse(
        message_id=response["MessageId"],
        md5_of_message_body=response["MD5OfMessageBody"],
    )
