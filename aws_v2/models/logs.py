"""
Data models for AWS CloudWatch Logs.
Contains dataclasses for logs input and output structures.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    filter_pattern: Optional[str] = None
    limit: Optional[int] = None


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
