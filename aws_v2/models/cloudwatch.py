"""
Data models for AWS CloudWatch.
Contains dataclasses for CloudWatch metrics and statistics.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class MetricStatisticsInput:
    """
    Represents the input parameters for fetching metric statistics.

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
    Represents the output of the metric statistics.

    Attributes:
        label (str): The label for the metric.
        datapoints (List[Dict[str, Any]]): The data points for the metric.
    """

    label: str
    datapoints: List[Dict[str, Any]]
