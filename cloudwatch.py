"module"

from datetime import datetime
from typing import Dict, List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("cloudwatch")


@pivot_exceptions
def get_metric_statistics(
    namespace: str,
    metric_name: str,
    dimensions: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    period: int,
    statistics: List[str],
    cloudwatch_client: boto3.client = client,
):
    "function"
    return cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics,
    )
