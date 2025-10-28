"""Unit tests for DynamoDB utility functions."""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.dynamodb import scan
from aws_v2.models.dynamodb import DynamoDBScanOutput


class TestDynamoDB(unittest.TestCase):
    """Test cases for DynamoDB utility functions."""

    def setUp(self):
        """Set up common test data for DynamoDB tests."""
        self.mock_dynamodb = MagicMock()
        # Mock response for a scan with no filter
        self.mock_scan_response = {
            "Items": [
                {
                    "id": {"S": "1"},
                    "name": {"S": "Item 1"},
                    "active": {"BOOL": True},
                },
                {
                    "id": {"S": "2"},
                    "name": {"S": "Item 2"},
                    "active": {"BOOL": False},
                },
            ],
            "Count": 2,
            "ScannedCount": 2,
            "ConsumedCapacity": {
                "TableName": "test-table",
                "CapacityUnits": 0.5,
            },
        }
        # Mock response for when pagination is needed
        self.mock_paginated_responses = [
            {
                "Items": [
                    {
                        "id": {"S": "1"},
                        "name": {"S": "Item 1"},
                        "active": {"BOOL": True},
                    }
                ],
                "Count": 1,
                "ScannedCount": 1,
                "LastEvaluatedKey": {"id": {"S": "1"}},
            },
            {
                "Items": [
                    {
                        "id": {"S": "2"},
                        "name": {"S": "Item 2"},
                        "active": {"BOOL": False},
                    }
                ],
                "Count": 1,
                "ScannedCount": 1,
                "ConsumedCapacity": {
                    "TableName": "test-table",
                    "CapacityUnits": 0.5,
                },
            },
        ]

    @patch("aws_v2.dynamodb.client")
    def test_scan_no_filter(self, mock_client):
        """Test scan function without filter expression."""
        # Configure the mock client
        mock_client.scan.return_value = self.mock_scan_response

        # Call the function
        result = scan(table_name="test-table")

        # Verify results
        self.assertIsInstance(result, DynamoDBScanOutput)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.count, 2)
        self.assertEqual(result.scanned_count, 2)
        self.assertEqual(
            result.consumed_capacity,
            self.mock_scan_response["ConsumedCapacity"],
        )
        self.assertIsNone(result.last_evaluated_key)

        # Verify the client was called correctly
        mock_client.scan.assert_called_once_with(TableName="test-table")

    @patch("aws_v2.dynamodb.client")
    def test_scan_with_filter(self, mock_client):
        """Test scan function with filter expression."""
        # Configure the mock client
        mock_client.scan.return_value = self.mock_scan_response

        # Test data
        filter_expression = "active = :active"
        expression_attr_val = {":active": {"BOOL": True}}

        # Call the function
        result = scan(
            table_name="test-table",
            filter_expression=filter_expression,
            expression_attr_val=expression_attr_val,
        )

        # Verify results
        self.assertIsInstance(result, DynamoDBScanOutput)
        self.assertEqual(len(result.items), 2)

        # Verify the client was called correctly with filters
        mock_client.scan.assert_called_once_with(
            TableName="test-table",
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attr_val,
        )

    @patch("aws_v2.dynamodb.client")
    def test_scan_with_pagination(self, mock_client):
        """Test scan function with pagination."""
        # Configure the mock client to return different responses on subsequent calls
        mock_client.scan.side_effect = self.mock_paginated_responses

        # Call the function
        result = scan(table_name="test-table")

        # Verify results
        self.assertIsInstance(result, DynamoDBScanOutput)
        self.assertEqual(
            len(result.items), 2
        )  # Combined items from both pages
        self.assertEqual(result.count, 2)  # Sum of counts from both pages
        self.assertEqual(
            result.scanned_count, 2
        )  # Sum of scanned counts from both pages

        # Verify the client was called twice (for both pages)
        self.assertEqual(mock_client.scan.call_count, 2)
        mock_client.scan.assert_any_call(TableName="test-table")
        mock_client.scan.assert_any_call(
            TableName="test-table",
            ExclusiveStartKey=self.mock_paginated_responses[0][
                "LastEvaluatedKey"
            ],
        )

    def test_scan_with_custom_client(self):
        """Test scan function with a custom client."""
        # Create a mock client
        custom_client = MagicMock()
        custom_client.scan.return_value = self.mock_scan_response

        # Call the function with the custom client
        result = scan(table_name="test-table", dynamodb_client=custom_client)

        # Verify results
        self.assertIsInstance(result, DynamoDBScanOutput)
        self.assertEqual(len(result.items), 2)

        # Verify the custom client was used instead of the default one
        custom_client.scan.assert_called_once_with(TableName="test-table")


if __name__ == "__main__":
    unittest.main()
