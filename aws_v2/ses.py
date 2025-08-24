"module"

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("ses")


@pivot_exceptions
def send_email(
    source: str,
    destination: dict,
    message: dict,
    ses_client: boto3.client = None,
) -> str:
    "function"
    if ses_client is None:
        ses_client = client
    return ses_client.send_email(
        Source=source, Destination=destination, Message=message
    )


@pivot_exceptions
def send_raw_email(raw_message: bytes, ses_client: boto3.client = None) -> dict:
    "function"
    if ses_client is None:
        ses_client = client
    return ses_client.send_raw_email(RawMessage={"Data": raw_message})
