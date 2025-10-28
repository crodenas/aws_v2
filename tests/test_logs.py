"""Unit tests for CloudWatch Logs utility functions."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from aws_v2.logs import FilterLogEventsInput, filter_log_events


class TestLogs(unittest.TestCase):
    """Test cases for CloudWatch Logs utility functions."""

    def setUp(self):
        """Set up common test data for Logs tests."""
        self.mock_logs_client = MagicMock()
        self.mock_paginator = MagicMock()
        self.mock_logs_client.get_paginator.return_value = self.mock_paginator
        self.start_time = datetime(2025, 8, 1)
        self.end_time = datetime(2025, 8, 24)
        self.inputs = FilterLogEventsInput(
            log_group_name="/aws/lambda/my-function",
            log_stream_name_prefix="2025/08",
            start_time=self.start_time,
            end_time=self.end_time,
            filter_pattern="ERROR",
            limit=100,
        )
        self.mock_paginator.paginate.return_value = [
            {
                "events": [
                    {
                        "timestamp": 1722528000000,
                        "message": "ERROR: Failed to process request",
                        "ingestionTime": 1722528001000,
                    },
                    {
                        "timestamp": 1722614400000,
                        "message": "ERROR: Database connection timeout",
                        "ingestionTime": 1722614401000,
                    },
                ]
            },
            {
                "events": [
                    {
                        "timestamp": 1724428800000,
                        "message": "ERROR: Internal server error",
                        "ingestionTime": 1724428801000,
                    }
                ]
            },
        ]

    @patch("aws_v2.logs.client")
    def test_filter_log_events(self, mock_client):
        """Test filter_log_events returns expected log events."""
        mock_client.get_paginator.return_value = self.mock_paginator
        result = filter_log_events(self.inputs, logs_client=mock_client)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].message, "ERROR: Failed to process request")

        # Call the function with the mock logs client
        result = filter_log_events(self.inputs, mock_client)

        # Verify the results
        self.assertEqual(len(result), 3)

        # Verify first log event
        self.assertEqual(result[0].timestamp, 1722528000000)
        self.assertEqual(result[0].message, "ERROR: Failed to process request")
        self.assertEqual(result[0].ingestion_time, 1722528001000)

        # Verify second log event
        self.assertEqual(result[1].timestamp, 1722614400000)
        self.assertEqual(
            result[1].message, "ERROR: Database connection timeout"
        )
        self.assertEqual(result[1].ingestion_time, 1722614401000)

        # Verify third log event
        self.assertEqual(result[2].timestamp, 1724428800000)
        self.assertEqual(result[2].message, "ERROR: Internal server error")
        self.assertEqual(result[2].ingestion_time, 1724428801000)

        # Verify the paginator was used correctly
        mock_client.get_paginator.assert_called_with("filter_log_events")
        self.assertEqual(mock_client.get_paginator.call_count, 2)

        self.assertEqual(self.mock_paginator.paginate.call_count, 2)

    def test_filter_log_events_with_minimal_inputs(self):
        """Test filter_log_events function with minimal required inputs."""
        # Create mock logs client
        mock_logs_client = MagicMock()
        mock_paginator = MagicMock()
        mock_logs_client.get_paginator.return_value = mock_paginator

        # Create minimal input object
        inputs = FilterLogEventsInput(
            log_group_name="/aws/lambda/minimal-function",
            log_stream_name_prefix="2025/08",
        )

        # Set up the mock paginator to return sample log events
        mock_paginator.paginate.return_value = [
            {
                "events": [
                    {
                        "timestamp": 1724515200000,  # August 24, 2025
                        "message": "Function execution completed",
                        "ingestionTime": 1724515201000,
                    }
                ]
            }
        ]

        # Call the function with the mock logs client
        result = filter_log_events(inputs, mock_logs_client)

        # Verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].timestamp, 1724515200000)
        self.assertEqual(result[0].message, "Function execution completed")
        self.assertEqual(result[0].ingestion_time, 1724515201000)

        # Verify the paginator was called with the correct parameters
        # Including None for optional parameters
        mock_paginator.paginate.assert_called_once_with(
            logGroupName="/aws/lambda/minimal-function",
            logStreamNamePrefix="2025/08",
            startTime=None,
            endTime=None,
            filterPattern=None,
            limit=None,
        )

    def test_filter_log_events_empty_results(self):
        """Test filter_log_events function when no logs match the criteria."""
        # Create mock logs client
        mock_logs_client = MagicMock()
        mock_paginator = MagicMock()
        mock_logs_client.get_paginator.return_value = mock_paginator

        # Create input object
        inputs = FilterLogEventsInput(
            log_group_name="/aws/lambda/empty-function",
            log_stream_name_prefix="2025/08",
            filter_pattern="CRITICAL",
        )

        # Set up the mock paginator to return empty results
        mock_paginator.paginate.return_value = [{"events": []}]

        # Call the function with the mock logs client
        result = filter_log_events(inputs, mock_logs_client)

        # Verify empty results
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
