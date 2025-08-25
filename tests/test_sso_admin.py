import unittest
from unittest.mock import patch

from aws_v2.sso_admin import (AccountAssignmentCreationStatus,
                              create_account_assignment)


class TestSSOAdmin(unittest.TestCase):

    @patch("aws_v2.sso_admin.client")
    def test_create_account_assignment(self, mock_client):
        # Mock the response from the boto3 client
        mock_response = {
            "AccountAssignment": {
                "Status": "SUCCEEDED",
                "RequestId": "12345",
                "CreatedDate": "2025-08-24T12:00:00Z",
                "FailureReason": None,
            }
        }
        mock_client.create_account_assignment.return_value = mock_response

        # Call the function
        result = create_account_assignment(
            instance_arn="arn:aws:sso:::instance/sso-instance-id",
            permission_set_arn="arn:aws:sso:::permissionSet/permission-set-id",
            principal_id="principal-id",
            target_id="target-id",
            principal_type="USER",
            sso_admin_client=mock_client,
        )

        # Assert the result
        self.assertIsInstance(result, AccountAssignmentCreationStatus)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(result.request_id, "12345")
        self.assertEqual(result.created_date, "2025-08-24T12:00:00Z")
        self.assertIsNone(result.failure_reason)


if __name__ == "__main__":
    unittest.main()
