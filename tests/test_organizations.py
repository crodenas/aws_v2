"""Unit tests for Organizations utility functions."""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.organizations import list_accounts


class TestOrganizations(unittest.TestCase):
    """Test cases for Organizations utility functions."""

    def setUp(self):
        """Set up common test data for Organizations tests."""
        self.mock_organizations = MagicMock()
        self.mock_paginator = MagicMock()
        self.mock_organizations.get_paginator.return_value = self.mock_paginator

        # Mock the paginate response with two pages
        self.mock_paginator.paginate.return_value = [
            {
                "Accounts": [
                    {
                        "Id": "123456789012",
                        "Arn": "arn:aws:organizations::123456789012:account/o-exampleorgid/123456789012",
                        "Name": "Master Account",
                        "Email": "main@example.com",
                        "Status": "ACTIVE",
                        "JoinedMethod": "CREATED",
                        "JoinedTimestamp": "2020-01-01T00:00:00Z",
                    },
                    {
                        "Id": "234567890123",
                        "Arn": "arn:aws:organizations::123456789012:account/o-exampleorgid/234567890123",
                        "Name": "Dev Account",
                        "Email": "dev@example.com",
                        "Status": "ACTIVE",
                        "JoinedMethod": "INVITED",
                        "JoinedTimestamp": "2020-02-01T00:00:00Z",
                    },
                ]
            },
            {
                "Accounts": [
                    {
                        "Id": "345678901234",
                        "Arn": "arn:aws:organizations::123456789012:account/o-exampleorgid/345678901234",
                        "Name": "Prod Account",
                        "Email": "prod@example.com",
                        "Status": "ACTIVE",
                        "JoinedMethod": "INVITED",
                        "JoinedTimestamp": "2020-03-01T00:00:00Z",
                    }
                ]
            },
        ]

    def test_list_accounts(self):
        """Test that list_accounts correctly aggregates all accounts."""
        # Call the function with our mock client
        result = list_accounts(self.mock_organizations)

        # Verify the paginator was called correctly
        self.mock_organizations.get_paginator.assert_called_once_with("list_accounts")
        self.mock_paginator.paginate.assert_called_once()

        # Verify the result contains all accounts from all pages
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].id, "123456789012")
        self.assertEqual(result[1].id, "234567890123")
        self.assertEqual(result[2].id, "345678901234")

    def test_list_accounts_empty_response(self):
        """Test that list_accounts handles empty responses correctly."""
        # Configure the mock to return empty responses
        self.mock_paginator.paginate.return_value = [
            {"Accounts": []},
            {},  # Missing 'Accounts' key
        ]

        # Call the function with our mock client
        result = list_accounts(self.mock_organizations)

        # Verify the result is an empty list
        self.assertEqual(result, [])

    @patch("aws_v2.organizations.client")
    def test_list_accounts_default_client(self, mock_default_client):
        """Test that list_accounts uses the default client when none is provided."""
        # Set up the default client mock
        mock_paginator = MagicMock()
        mock_default_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [
            {
                "Accounts": [
                    {
                        "Id": "123456789012",
                        "Arn": "arn:aws:organizations::123456789012:account/o-exampleorgid/123456789012",
                        "Name": "Master Account",
                        "Email": "main@example.com",
                        "Status": "ACTIVE",
                        "JoinedMethod": "CREATED",
                        "JoinedTimestamp": "2020-01-01T00:00:00Z",
                    }
                ]
            }
        ]

        # Call the function without providing a client twice to match the original test logic
        result1 = list_accounts()
        result2 = list_accounts()

        # Verify the default client was used twice
        self.assertEqual(mock_default_client.get_paginator.call_count, 2)

        # Verify the results
        self.assertEqual(len(result1), 1)
        self.assertEqual(result1[0].id, "123456789012")
        self.assertEqual(len(result2), 1)
        self.assertEqual(result2[0].id, "123456789012")
        # Set up the default client mock
        mock_paginator = MagicMock()
        mock_default_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = [
            {
                "Accounts": [
                    {
                        "Id": "123456789012",
                        "Arn": "arn:aws:organizations::123456789012:account/o-exampleorgid/123456789012",
                        "Name": "Master Account",
                        "Email": "main@example.com",
                        "Status": "ACTIVE",
                        "JoinedMethod": "CREATED",
                        "JoinedTimestamp": "2020-01-01T00:00:00Z",
                    }
                ]
            }
        ]

        # Call the function without providing a client


if __name__ == "__main__":
    unittest.main()
