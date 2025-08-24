import unittest
from datetime import datetime
from unittest.mock import patch

from aws_v2.cloudwatch import (MetricStatisticsInput, MetricStatisticsOutput,
                               get_metric_statistics)


class TestCloudWatch(unittest.TestCase):

    @patch("aws_v2.cloudwatch.client")
    def test_get_metric_statistics(self, mock_client):
        """
        Test the get_metric_statistics function.
        """
        # Mock input data
        input_data = MetricStatisticsInput(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions=[{"Name": "InstanceId", "Value": "i-1234567890abcdef0"}],
            start_time=datetime(2025, 8, 23, 0, 0),
            end_time=datetime(2025, 8, 24, 0, 0),
            period=300,
            statistics=["Average"],
        )

        # Mock response
        mock_response = {
            "Label": "CPUUtilization",
            "Datapoints": [
                {"Timestamp": "2025-08-23T00:05:00Z", "Average": 15.0},
                {"Timestamp": "2025-08-23T00:10:00Z", "Average": 20.0},
            ],
        }
        mock_client.get_metric_statistics.return_value = mock_response

        # Call the function
        result = get_metric_statistics(input_data, cloudwatch_client=mock_client)

        # Assertions
        self.assertIsInstance(result, MetricStatisticsOutput)
        self.assertEqual(result.label, "CPUUtilization")
        self.assertEqual(len(result.datapoints), 2)
        self.assertEqual(result.datapoints[0]["Average"], 15.0)
        self.assertEqual(result.datapoints[1]["Average"], 20.0)

        # Verify the call
        mock_client.get_metric_statistics.assert_called_once_with(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": "i-1234567890abcdef0"}],
            StartTime=input_data.start_time,
            EndTime=input_data.end_time,
            Period=300,
            Statistics=["Average"],
        )


if __name__ == "__main__":
    unittest.main()
