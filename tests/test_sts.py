import unittest
from unittest.mock import patch

from aws_v2 import CredentialsObject, sts
from aws_v2.sts import (
    AssumedRoleUserObject,
    AssumeRoleResponse,
    CallerIdentityResponse,
)


class TestSTS(unittest.TestCase):
    @patch("aws_v2.sts.client")
    def test_get_caller_identity(self, mock_client):
        mock_response = {
            "Account": "123456789012",
            "UserId": "AIDAEXAMPLE",
            "Arn": "arn:aws:iam::123456789012:user/example",
        }
        mock_client.get_caller_identity.return_value = mock_response
        result = sts.get_caller_identity(sts_client=mock_client)
        self.assertIsInstance(result, CallerIdentityResponse)
        self.assertEqual(result.account, "123456789012")
        self.assertEqual(result.user_id, "AIDAEXAMPLE")
        self.assertEqual(result.arn, "arn:aws:iam::123456789012:user/example")

    @patch("aws_v2.sts.client")
    def test_assume_role(self, mock_client):
        mock_response = {
            "Credentials": {
                "AccessKeyId": "AKIAEXAMPLE",
                "SecretAccessKey": "secret",
                "SessionToken": "token",
                "Expiration": "2025-08-25T12:00:00Z",
            },
            "AssumedRoleUser": {
                "AssumedRoleId": "AROEXAMPLE:session",
                "Arn": (
                    "arn:aws:sts::123456789012:"
                    "assumed-role/example-role/session"
                ),
            },
        }
        mock_client.assume_role.return_value = mock_response
        # CredentialsObject expects all keys in Credentials
        with patch(
            "aws_v2.sts.CredentialsObject",
            side_effect=lambda **kwargs: CredentialsObject(
                access_key_id=kwargs.get("AccessKeyId"),
                secret_access_key=kwargs.get("SecretAccessKey"),
                session_token=kwargs.get("SessionToken"),
                expiration=kwargs.get("Expiration"),
            ),
        ):
            result = sts.assume_role(
                "arn:aws:iam::123456789012:role/example-role",
                sts_client=mock_client,
            )
        self.assertIsInstance(result, AssumeRoleResponse)
        self.assertIsInstance(result.credentials, CredentialsObject)
        self.assertIsInstance(result.assumed_role_user, AssumedRoleUserObject)
        self.assertEqual(
            result.assumed_role_user.arn,
            "arn:aws:sts::123456789012:assumed-role/example-role/session",
        )


if __name__ == "__main__":
    unittest.main()
