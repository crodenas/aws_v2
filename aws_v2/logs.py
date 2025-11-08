"""
This module provides functionality for interacting with AWS CloudWatch Logs.
It includes functionality to filter log events.
"""

from typing import List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.logs import FilterLogEventsInput, LogEvent

client = session.client("logs")


@pivot_exceptions
def filter_log_events(
    inputs: FilterLogEventsInput,
    logs_client: Optional[boto3.client] = None,
) -> List[LogEvent]:
    """
    Filters log events from AWS CloudWatch Logs based on the provided
    input parameters.

    Args:
        inputs: The input parameters for filtering log events.
        logs_client: The boto3 client for CloudWatch Logs. Defaults to
            module client.

    Returns:
        A list of log events matching the filter criteria.
    """
    if logs_client is None:
        logs_client = client

    events = []
    payload = {
        "logGroupName": inputs.log_group_name,
        "logStreamNamePrefix": inputs.log_stream_name_prefix,
        "startTime": inputs.start_time,
        "endTime": inputs.end_time,
        "filterPattern": inputs.filter_pattern,
        "limit": inputs.limit,
    }

    paginator = logs_client.get_paginator("filter_log_events")
    for page in paginator.paginate(**payload):
        for event in page["events"]:
            events.append(
                LogEvent(
                    timestamp=event["timestamp"],
                    message=event["message"],
                    ingestion_time=event["ingestionTime"],
                )
            )

    return events
