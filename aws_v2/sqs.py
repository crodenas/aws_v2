"module"

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("sqs")


def get_region_from_url(url: str) -> str:
    "function"
    return url.split(".")[1]


@pivot_exceptions
def send_message(
    queue_url: str, message_body: str, sqs_client: boto3.client = client
) -> dict:
    "function"
    return sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
