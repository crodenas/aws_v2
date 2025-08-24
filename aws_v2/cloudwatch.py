"""
This module provides utilities for interacting with AWS CloudWatch.

It includes functions to fetch metric statistics using the AWS SDK (boto3).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("cloudwatch")


@dataclass
class MetricStatisticsInput:
    """
    Dataclass representing the input parameters for fetching metric statistics.

    Attributes:
        namespace (str): The namespace of the metric.
        metric_name (str): The name of the metric.
        dimensions (List[Dict[str, str]]): The dimensions for the metric.
        start_time (datetime): The start time for the metric data.
        end_time (datetime): The end time for the metric data.
        period (int): The granularity, in seconds, of the returned data points.
        statistics (List[str]): The metric statistics to retrieve (e.g., Average, Sum).
    """

    namespace: str
    metric_name: str
    dimensions: List[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    period: int
    statistics: List[str]


@dataclass
class MetricStatisticsOutput:
    """
    Dataclass representing the output of the metric statistics.

    Attributes:
        label (str): The label for the metric.
        datapoints (List[Dict[str, Any]]): The data points for the metric.
    """

    label: str
    datapoints: List[Dict[str, Any]]


@pivot_exceptions
def get_metric_statistics(
    input_data: MetricStatisticsInput,
    cloudwatch_client: boto3.client = None,
) -> MetricStatisticsOutput:
    """
    Fetch metric statistics from AWS CloudWatch.

    Args:
        input_data (MetricStatisticsInput): Dataclass containing input parameters.
        cloudwatch_client (boto3.client, optional): CloudWatch client. Defaults to None.

    Returns:
        MetricStatisticsOutput: Dataclass containing the response from CloudWatch.

    Raises:
        Exception: If an error occurs while fetching the metric statistics.
    """
    if cloudwatch_client is None:
        cloudwatch_client = client

    response = cloudwatch_client.get_metric_statistics(
        Namespace=input_data.namespace,
        MetricName=input_data.metric_name,
        Dimensions=input_data.dimensions,
        StartTime=input_data.start_time,
        EndTime=input_data.end_time,
        Period=input_data.period,
        Statistics=input_data.statistics,
    )

    return MetricStatisticsOutput(
        label=response.get("Label"),
        datapoints=response.get("Datapoints", []),
    )
