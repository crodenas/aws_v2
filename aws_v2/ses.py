"""
This module provides functionality for sending emails using AWS SES (Simple Email Service).
It includes functions for sending both standard and raw emails.
"""

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.ses import Email, EmailResponse, RawEmailResponse

client = session.client("ses")


@pivot_exceptions
def send_email(
    email: Email,
    ses_client: boto3.client = None,
) -> EmailResponse:
    """
    Sends an email using AWS SES.

    Args:
        email (Email): The email data to be sent.
        ses_client (boto3.client, optional): A custom SES client. Defaults to
            the module-level client.

    Returns:
        EmailResponse: The response from the SES service.
    """
    if ses_client is None:
        ses_client = client
    response = ses_client.send_email(
        Source=email.source,
        Destination=email.destination,
        Message=email.message,
    )
    return EmailResponse(
        message_id=response["MessageId"],
        response_metadata=response["ResponseMetadata"],
    )


@pivot_exceptions
def send_raw_email(
    raw_message: bytes, ses_client: boto3.client = None
) -> RawEmailResponse:
    """
    Sends a raw email using AWS SES.

    Args:
        raw_message (bytes): The raw email data to be sent.
        ses_client (boto3.client, optional): A custom SES client. Defaults to the
            module-level client.

    Returns:
        RawEmailResponse: The response from the SES service.
    """
    if ses_client is None:
        ses_client = client
    response = ses_client.send_raw_email(RawMessage={"Data": raw_message})
    return RawEmailResponse(
        message_id=response["MessageId"],
        response_metadata=response["ResponseMetadata"],
    )
