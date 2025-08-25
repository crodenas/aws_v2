import unittest
from unittest.mock import patch, MagicMock
import aws_v2.ses as ses


class TestSES(unittest.TestCase):
    def setUp(self):
        self.email = ses.Email(
            source="sender@example.com",
            destination={"ToAddresses": ["recipient@example.com"]},
            message={
                "Subject": {"Data": "Test Subject"},
                "Body": {"Text": {"Data": "Test Body"}},
            },
        )
        self.raw_message = b"Raw email content"

    @patch("aws_v2.ses.client")
    def test_send_email_success(self, mock_client):
        mock_response = {
            "MessageId": "test-message-id",
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        mock_client.send_email.return_value = mock_response
        response = ses.send_email(self.email)
        self.assertIsInstance(response, ses.EmailResponse)
        self.assertEqual(response.message_id, "test-message-id")
        self.assertEqual(response.response_metadata["HTTPStatusCode"], 200)

    @patch("aws_v2.ses.client")
    def test_send_raw_email_success(self, mock_client):
        mock_response = {
            "MessageId": "raw-message-id",
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        mock_client.send_raw_email.return_value = mock_response
        response = ses.send_raw_email(self.raw_message)
        self.assertIsInstance(response, ses.RawEmailResponse)
        self.assertEqual(response.message_id, "raw-message-id")
        self.assertEqual(response.response_metadata["HTTPStatusCode"], 200)

    @patch("aws_v2.ses.client")
    def test_send_email_with_custom_client(self, mock_client):
        mock_response = {
            "MessageId": "custom-client-id",
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        mock_client.send_email.return_value = mock_response
        response = ses.send_email(self.email, ses_client=mock_client)
        self.assertEqual(response.message_id, "custom-client-id")

    @patch("aws_v2.ses.client")
    def test_send_raw_email_with_custom_client(self, mock_client):
        mock_response = {
            "MessageId": "custom-raw-id",
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        mock_client.send_raw_email.return_value = mock_response
        response = ses.send_raw_email(self.raw_message, ses_client=mock_client)
        self.assertEqual(response.message_id, "custom-raw-id")


if __name__ == "__main__":
    unittest.main()
