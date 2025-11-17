"""
This module provides utilities for interacting with AWS SQS (Simple Queue
Service).

It includes functions for extracting the region from an SQS URL and sending
messages to an SQS queue.
"""

from typing import Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.sqs import SQSMessageResponse, SQSMessage

client = session.client("sqs")


def get_region_from_url(url: str) -> str:
    """
    Extract the AWS region from an SQS queue URL.

    Args:
        url: The SQS queue URL.

    Returns:
        The AWS region extracted from the URL.
    """
    return url.split(".")[1]


@pivot_exceptions
def send_message(
    queue_url: str,
    message_body: str,
    sqs_client: Optional[boto3.client] = None,
) -> SQSMessageResponse:
    """
    Send a message to an SQS queue.

    Args:
        queue_url: The URL of the SQS queue.
        message_body: The content of the message to send.
        sqs_client: A custom SQS client. Defaults to the module's
            client.

    Returns:
        The response containing the message ID and MD5 checksum.
    """
    if sqs_client is None:
        sqs_client = client
    response = sqs_client.send_message(
        QueueUrl=queue_url, MessageBody=message_body
    )
    return SQSMessageResponse(
        message_id=response["MessageId"],
        md5_of_message_body=response["MD5OfMessageBody"],
    )


@pivot_exceptions
def receive_message(
    queue_url: str,
    max_number_of_messages: int = 1,
    wait_time_seconds: int = 0,
    sqs_client: Optional[boto3.client] = None,
) -> list[SQSMessage]:
    """
    Receive messages from an SQS queue.

    Args:
        queue_url: The URL of the SQS queue.
        max_number_of_messages: The maximum number of messages to retrieve.
        wait_time_seconds: The duration (in seconds) for which the call waits
            for a message to arrive in the queue before returning.
        sqs_client: A custom SQS client. Defaults to the module's
            client.
    """
    if sqs_client is None:
        sqs_client = client
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=["All"],
    )
    messages = response.get("Messages", [])
    return [
        SQSMessage(
            message_id=msg["MessageId"],
            receipt_handle=msg["ReceiptHandle"],
            body=msg["Body"],
        )
        for msg in messages
    ]


@pivot_exceptions
def delete_message(
    queue_url: str,
    receipt_handle: str,
    sqs_client: Optional[boto3.client] = None,
) -> None:
    """
    Delete a message from an SQS queue.

    Args:
        queue_url: The URL of the SQS queue.
        receipt_handle: The receipt handle associated with the message to delete.
        sqs_client: A custom SQS client. Defaults to the module's
            client.
    """
    if sqs_client is None:
        sqs_client = client
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )
