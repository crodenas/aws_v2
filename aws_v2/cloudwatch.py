"""
This module provides utilities for interacting with AWS CloudWatch.

It includes functions to fetch metric statistics using the AWS SDK (boto3).
"""

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.cloudwatch import MetricStatisticsInput, MetricStatisticsOutput

client = session.client("cloudwatch")


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
