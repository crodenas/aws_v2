import unittest
from unittest.mock import MagicMock, patch

from aws_v2 import utils
from aws_v2.models.base import CredentialsObject


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.mock_credentials = CredentialsObject(
            access_key_id="AKIAEXAMPLE",
            secret_access_key="secret",
            session_token="token",
            expiration="2025-08-25T12:00:00Z",
        )
        self.role_arn = "arn:aws:iam::123456789012:role/example-role"
        self.region_name = "us-west-2"

    @patch("aws_v2.utils.get_session")
    @patch("aws_v2.utils.sts")
    def test_assume_role_with_region(self, mock_sts, mock_get_session):
        """Test assume_role with specified region."""
        mock_sts.assume_role.return_value = MagicMock(
            credentials=self.mock_credentials
        )
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        result = utils.assume_role(self.role_arn, region_name=self.region_name)

        mock_sts.assume_role.assert_called_once_with(role_arn=self.role_arn)
        mock_get_session.assert_called_once_with(
            self.mock_credentials, region_name=self.region_name
        )
        self.assertEqual(result, mock_session)

    @patch("aws_v2.utils.get_session")
    @patch("aws_v2.utils.sts")
    def test_assume_role_default_region(self, mock_sts, mock_get_session):
        """Test assume_role uses default region when none specified."""
        mock_sts.session.region_name = "us-east-1"
        mock_sts.assume_role.return_value = MagicMock(
            credentials=self.mock_credentials
        )
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        result = utils.assume_role(self.role_arn)

        mock_sts.assume_role.assert_called_once_with(role_arn=self.role_arn)
        mock_get_session.assert_called_once_with(
            self.mock_credentials, region_name="us-east-1"
        )
        self.assertEqual(result, mock_session)

    @patch("aws_v2.utils.assume_role")
    def test_get_client_with_role_with_region(self, mock_assume_role):
        """Test get_client_with_role with specified region."""
        mock_session = MagicMock()
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client
        mock_assume_role.return_value = mock_session

        result = utils.get_client_with_role(
            "s3", self.role_arn, region_name=self.region_name
        )

        mock_assume_role.assert_called_once_with(
            role_arn=self.role_arn, region_name=self.region_name
        )
        mock_session.client.assert_called_once_with("s3")
        self.assertEqual(result, mock_client)

    @patch("aws_v2.utils.assume_role")
    def test_get_client_with_role_default_region(self, mock_assume_role):
        """Test get_client_with_role uses default region when none specified."""
        mock_session = MagicMock()
        mock_client = MagicMock()
        mock_session.client.return_value = mock_client
        mock_assume_role.return_value = mock_session

        result = utils.get_client_with_role("s3", self.role_arn)

        mock_assume_role.assert_called_once_with(
            role_arn=self.role_arn, region_name=None
        )
        mock_session.client.assert_called_once_with("s3")
        self.assertEqual(result, mock_client)

    @patch("botocore.waiter.create_waiter_with_client")
    @patch("botocore.waiter.WaiterModel")
    def test_create_waiter_with_client(
        self, mock_waiter_model, mock_create_waiter
    ):
        """Test create_waiter with custom client."""
        waiter_config = {"delay": 5, "maxAttempts": 10}
        mock_client = MagicMock()
        mock_waiter = MagicMock()
        mock_waiter_model_instance = MagicMock()
        mock_waiter_model.return_value = mock_waiter_model_instance
        mock_create_waiter.return_value = mock_waiter

        result = utils.create_waiter(
            "test_waiter", waiter_config, client=mock_client
        )

        mock_waiter_model.assert_called_once_with(waiter_config)
        mock_create_waiter.assert_called_once_with(
            "test_waiter", mock_waiter_model_instance, mock_client
        )
        self.assertEqual(result, mock_waiter)

    @patch("botocore.waiter.create_waiter_with_client")
    @patch("botocore.waiter.WaiterModel")
    def test_create_waiter_without_client(
        self, mock_waiter_model, mock_create_waiter
    ):
        """Test create_waiter without client (defaults to None)."""
        waiter_config = {"delay": 5, "maxAttempts": 10}
        mock_waiter = MagicMock()
        mock_waiter_model_instance = MagicMock()
        mock_waiter_model.return_value = mock_waiter_model_instance
        mock_create_waiter.return_value = mock_waiter

        result = utils.create_waiter("test_waiter", waiter_config)

        mock_waiter_model.assert_called_once_with(waiter_config)
        mock_create_waiter.assert_called_once_with(
            "test_waiter", mock_waiter_model_instance, None
        )
        self.assertEqual(result, mock_waiter)

    @patch("aws_v2.utils.sts")
    def test_validate_credentials_success(self, mock_sts):
        """Test validate_credentials returns True when credentials are valid."""
        mock_sts.get_caller_identity.return_value = MagicMock()

        result = utils.validate_credentials()

        mock_sts.get_caller_identity.assert_called_once()
        self.assertTrue(result)

    @patch("aws_v2.utils.sts")
    def test_validate_credentials_failure(self, mock_sts):
        """Test validate_credentials raises AwsError when credentials are invalid."""
        from aws_v2.exceptions import AwsError

        mock_sts.get_caller_identity.side_effect = Exception(
            "Invalid credentials"
        )

        with self.assertRaises(AwsError) as context:
            utils.validate_credentials()

        self.assertIn(
            "AWS credentials validation failed", str(context.exception)
        )
        self.assertIn("Invalid credentials", str(context.exception))
        mock_sts.get_caller_identity.assert_called_once()


if __name__ == "__main__":
    unittest.main()
