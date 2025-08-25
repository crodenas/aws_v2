"""
This module provides functionality for interacting with AWS CloudWatch Logs.
It includes data classes for input and output structures and a function to filter log events.
"""

from datetime import datetime
from typing import List
from dataclasses import dataclass

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("logs")


@dataclass
class FilterLogEventsInput:
    """
    Represents the input parameters for filtering log events.

    Attributes:
        log_group_name (str): The name of the log group.
        log_stream_name_prefix (str): The prefix of the log stream name.
        start_time (datetime, optional): The start time for filtering logs.
        end_time (datetime, optional): The end time for filtering logs.
        filter_pattern (str, optional): The filter pattern to use.
        limit (int, optional): The maximum number of log events to return.
    """

    log_group_name: str
    log_stream_name_prefix: str
    start_time: datetime = None
    end_time: datetime = None
    filter_pattern: str = None
    limit: int = None


@dataclass
class LogEvent:
    """
    Represents a log event retrieved from CloudWatch Logs.

    Attributes:
        timestamp (int): The timestamp of the log event.
        message (str): The message of the log event.
        ingestion_time (int): The ingestion time of the log event.
    """

    timestamp: int
    message: str
    ingestion_time: int


@pivot_exceptions
def filter_log_events(
    inputs: FilterLogEventsInput,
    logs_client: boto3.client = None,
) -> List[LogEvent]:
    """
    Filters log events from AWS CloudWatch Logs based on the provided input parameters.

    Args:
        inputs (FilterLogEventsInput): The input parameters for filtering log events.
        logs_client (boto3.client, optional): The boto3 client for CloudWatch Logs.
            Defaults to None.

    Returns:
        List[LogEvent]: A list of log events matching the filter criteria.
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
