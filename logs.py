"Module"

# TODO - This module is NOT complete.
from datetime import datetime
from typing import Dict, List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("logs")


@pivot_exceptions
def filter_log_events(
    log_group_name: str,
    log_stream_name_prefix: str,
    start_time: datetime = None,
    end_time: datetime = None,
    filter_pattern: str = None,
    limit: int = None,
    logs_client: boto3.client = client,
) -> List[Dict]:
    "function"

    events = []
    payload = {
        "logGroupName": log_group_name,
        "logStreamNamePrefix": log_stream_name_prefix,
        "startTime": start_time,
        "endTime": end_time,
        "filterPattern": filter_pattern,
        "limit": limit,
    }

    paginator = logs_client.get_paginator("filter_log_events")
    for page in paginator.paginate(**payload):
        for event in page["events"]:
            events.append(event)

    return events
