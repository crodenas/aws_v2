"""Unit tests for S3 utility functions."""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from aws_v2.s3 import get_object, list_buckets, list_bucket_contents


class TestS3(unittest.TestCase):
    """Test cases for S3 utility functions."""

    def test_get_object(self):
        """Test the get_object function."""
        # Create mock S3 client
        mock_s3 = MagicMock()

        # Create mock response with required fields
        mock_body = MagicMock()
        mock_response = {
            "Body": mock_body,
            "ContentType": "text/plain",
            "ContentLength": 1024,
            "LastModified": datetime(2025, 8, 24, 12, 0, 0),
            "ETag": '"abcdef1234567890"',
        }
        mock_s3.get_object.return_value = mock_response

        # Call the function with the mock S3 client
        result = get_object("test-bucket", "test-key", mock_s3)

        # Verify the results
        self.assertEqual(result.body, mock_body)
        self.assertEqual(result.content_type, "text/plain")
        self.assertEqual(result.content_length, 1024)
        self.assertEqual(result.last_modified, datetime(2025, 8, 24, 12, 0, 0))
        self.assertEqual(result.etag, '"abcdef1234567890"')

        # Verify the S3 client was called correctly
        mock_s3.get_object.assert_called_once_with(Bucket="test-bucket", Key="test-key")

    def test_list_buckets(self):
        """Test the list_buckets function."""
        # Create mock S3 client
        mock_s3 = MagicMock()
        mock_paginator = MagicMock()
        mock_s3.get_paginator.return_value = mock_paginator

        # Set up mock paginator to return sample buckets
        mock_paginator.paginate.return_value = [
            {
                "Buckets": [
                    {
                        "Name": "test-bucket-1",
                        "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
                    },
                    {
                        "Name": "test-bucket-2",
                        "CreationDate": datetime(2025, 2, 2, 12, 0, 0),
                    },
                ]
            },
            {
                "Buckets": [
                    {
                        "Name": "test-bucket-3",
                        "CreationDate": datetime(2025, 3, 3, 12, 0, 0),
                    }
                ]
            },
        ]

        # Call the function with the mock S3 client
        result = list_buckets(mock_s3)

        # Verify the results
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "test-bucket-1")
        self.assertEqual(result[0].creation_date, datetime(2025, 1, 1, 12, 0, 0))
        self.assertEqual(result[1].name, "test-bucket-2")
        self.assertEqual(result[1].creation_date, datetime(2025, 2, 2, 12, 0, 0))
        self.assertEqual(result[2].name, "test-bucket-3")
        self.assertEqual(result[2].creation_date, datetime(2025, 3, 3, 12, 0, 0))

        # Verify the paginator was used correctly
        mock_s3.get_paginator.assert_called_once_with("list_buckets")
        mock_paginator.paginate.assert_called_once()

    def test_list_bucket_contents(self):
        """Test the list_bucket_contents function."""
        # Create mock S3 client
        mock_s3 = MagicMock()
        mock_paginator = MagicMock()
        mock_s3.get_paginator.return_value = mock_paginator

        # Set up mock paginator to return sample objects
        mock_paginator.paginate.return_value = [
            {"Contents": [{"Key": "test-object-1"}, {"Key": "test-object-2"}]},
            {"Contents": [{"Key": "test-object-3"}]},
        ]

        # Call the function with the mock S3 client
        result = list_bucket_contents("test-bucket", mock_s3)

        # Verify the results
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].key, "test-object-1")
        self.assertEqual(result[1].key, "test-object-2")
        self.assertEqual(result[2].key, "test-object-3")

        # Verify the paginator was used correctly
        mock_s3.get_paginator.assert_called_once_with("list_objects_v2")
        mock_paginator.paginate.assert_called_once_with(Bucket="test-bucket")

    @patch("aws_v2.s3.client")
    def test_get_object_with_default_client(self, mock_client):
        """Test the get_object function with the default client."""
        # Create mock response
        mock_body = MagicMock()
        mock_response = {
            "Body": mock_body,
            "ContentType": "text/plain",
            "ContentLength": 1024,
            "LastModified": datetime(2025, 8, 24, 12, 0, 0),
            "ETag": '"abcdef1234567890"',
        }
        mock_client.get_object.return_value = mock_response

        # Call the function with the default client
        result = get_object("test-bucket", "test-key")

        # Verify the results
        self.assertEqual(result.body, mock_body)
        self.assertEqual(result.content_type, "text/plain")
        self.assertEqual(result.content_length, 1024)
        self.assertEqual(result.last_modified, datetime(2025, 8, 24, 12, 0, 0))
        self.assertEqual(result.etag, '"abcdef1234567890"')

        # Verify the client was called correctly
        mock_client.get_object.assert_called_once_with(
            Bucket="test-bucket", Key="test-key"
        )

    @patch("aws_v2.s3.client")
    def test_list_buckets_with_default_client(self, mock_client):
        """Test the list_buckets function with the default client."""
        # Set up mock paginator
        mock_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator

        # Set up mock paginator response
        mock_paginator.paginate.return_value = [
            {
                "Buckets": [
                    {
                        "Name": "test-bucket-1",
                        "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
                    }
                ]
            }
        ]

        # Call the function with the default client
        result = list_buckets()

        # Verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "test-bucket-1")
        self.assertEqual(result[0].creation_date, datetime(2025, 1, 1, 12, 0, 0))

        # Verify the paginator was used correctly
        mock_client.get_paginator.assert_called_once_with("list_buckets")
        mock_paginator.paginate.assert_called_once()

    @patch("aws_v2.s3.client")
    def test_list_bucket_contents_with_default_client(self, mock_client):
        """Test the list_bucket_contents function with the default client."""
        # Set up mock paginator
        mock_paginator = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator

        # Set up mock paginator response
        mock_paginator.paginate.return_value = [
            {"Contents": [{"Key": "test-object-1"}]}
        ]

        # Call the function with the default client
        result = list_bucket_contents("test-bucket")

        # Verify the results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].key, "test-object-1")

        # Verify the paginator was used correctly
        mock_client.get_paginator.assert_called_once_with("list_objects_v2")
        mock_paginator.paginate.assert_called_once_with(Bucket="test-bucket")


if __name__ == "__main__":
    unittest.main()
