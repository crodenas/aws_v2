"""Unit tests for the sqs module in aws_v2 package."""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.models.sqs import SQSMessage, SQSMessageResponse
from aws_v2.sqs import (
    delete_message,
    get_region_from_url,
    receive_message,
    send_message,
)


class TestSQS(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.queue_url = (
            "https://sqs.us-west-2.amazonaws.com/123456789012/test-queue"
        )
        self.message_body = "Test message body"
        self.receipt_handle = "test-receipt-handle"
        self.message_id = "test-message-id"
        self.md5_checksum = "test-md5-checksum"

    def test_get_region_from_url(self):
        """Test extracting region from SQS queue URL."""
        url = "https://sqs.us-west-2.amazonaws.com/123456789012/my-queue"
        region = get_region_from_url(url)
        self.assertEqual(region, "us-west-2")

    def test_get_region_from_url_different_region(self):
        """Test extracting different region from SQS queue URL."""
        url = "https://sqs.eu-central-1.amazonaws.com/123456789012/my-queue"
        region = get_region_from_url(url)
        self.assertEqual(region, "eu-central-1")

    @patch("aws_v2.sqs.client")
    def test_send_message_success(self, mock_client):
        """Test sending a message successfully."""
        mock_response = {
            "MessageId": self.message_id,
            "MD5OfMessageBody": self.md5_checksum,
        }
        mock_client.send_message.return_value = mock_response

        response = send_message(self.queue_url, self.message_body)

        self.assertIsInstance(response, SQSMessageResponse)
        self.assertEqual(response.message_id, self.message_id)
        self.assertEqual(response.md5_of_message_body, self.md5_checksum)
        mock_client.send_message.assert_called_once_with(
            QueueUrl=self.queue_url, MessageBody=self.message_body
        )

    @patch("aws_v2.sqs.client")
    def test_send_message_with_custom_client(self, mock_client):
        """Test sending a message with a custom SQS client."""
        custom_client = MagicMock()
        mock_response = {
            "MessageId": "custom-message-id",
            "MD5OfMessageBody": "custom-md5",
        }
        custom_client.send_message.return_value = mock_response

        response = send_message(
            self.queue_url, self.message_body, sqs_client=custom_client
        )

        self.assertEqual(response.message_id, "custom-message-id")
        self.assertEqual(response.md5_of_message_body, "custom-md5")
        custom_client.send_message.assert_called_once_with(
            QueueUrl=self.queue_url, MessageBody=self.message_body
        )
        mock_client.send_message.assert_not_called()

    @patch("aws_v2.sqs.client")
    def test_receive_message_success(self, mock_client):
        """Test receiving messages successfully."""
        mock_response = {
            "Messages": [
                {
                    "MessageId": self.message_id,
                    "ReceiptHandle": self.receipt_handle,
                    "Body": self.message_body,
                }
            ]
        }
        mock_client.receive_message.return_value = mock_response

        messages = receive_message(self.queue_url)

        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], SQSMessage)
        self.assertEqual(messages[0].message_id, self.message_id)
        self.assertEqual(messages[0].receipt_handle, self.receipt_handle)
        self.assertEqual(messages[0].body, self.message_body)
        mock_client.receive_message.assert_called_once_with(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=0,
            MessageAttributeNames=["All"],
        )

    @patch("aws_v2.sqs.client")
    def test_receive_message_multiple(self, mock_client):
        """Test receiving multiple messages."""
        mock_response = {
            "Messages": [
                {
                    "MessageId": "msg-1",
                    "ReceiptHandle": "handle-1",
                    "Body": "body-1",
                },
                {
                    "MessageId": "msg-2",
                    "ReceiptHandle": "handle-2",
                    "Body": "body-2",
                },
            ]
        }
        mock_client.receive_message.return_value = mock_response

        messages = receive_message(
            self.queue_url, max_number_of_messages=5, wait_time_seconds=10
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].message_id, "msg-1")
        self.assertEqual(messages[1].message_id, "msg-2")
        mock_client.receive_message.assert_called_once_with(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10,
            MessageAttributeNames=["All"],
        )

    @patch("aws_v2.sqs.client")
    def test_receive_message_empty_queue(self, mock_client):
        """Test receiving messages from an empty queue."""
        mock_response = {}
        mock_client.receive_message.return_value = mock_response

        messages = receive_message(self.queue_url)

        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 0)

    @patch("aws_v2.sqs.client")
    def test_receive_message_with_custom_client(self, mock_client):
        """Test receiving messages with a custom SQS client."""
        custom_client = MagicMock()
        mock_response = {
            "Messages": [
                {
                    "MessageId": "custom-msg",
                    "ReceiptHandle": "custom-handle",
                    "Body": "custom-body",
                }
            ]
        }
        custom_client.receive_message.return_value = mock_response

        messages = receive_message(self.queue_url, sqs_client=custom_client)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message_id, "custom-msg")
        custom_client.receive_message.assert_called_once()
        mock_client.receive_message.assert_not_called()

    @patch("aws_v2.sqs.client")
    def test_delete_message_success(self, mock_client):
        """Test deleting a message successfully."""
        mock_client.delete_message.return_value = {}

        result = delete_message(self.queue_url, self.receipt_handle)

        self.assertIsNone(result)
        mock_client.delete_message.assert_called_once_with(
            QueueUrl=self.queue_url,
            ReceiptHandle=self.receipt_handle,
        )

    @patch("aws_v2.sqs.client")
    def test_delete_message_with_custom_client(self, mock_client):
        """Test deleting a message with a custom SQS client."""
        custom_client = MagicMock()
        custom_client.delete_message.return_value = {}

        result = delete_message(
            self.queue_url, self.receipt_handle, sqs_client=custom_client
        )

        self.assertIsNone(result)
        custom_client.delete_message.assert_called_once_with(
            QueueUrl=self.queue_url,
            ReceiptHandle=self.receipt_handle,
        )
        mock_client.delete_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
