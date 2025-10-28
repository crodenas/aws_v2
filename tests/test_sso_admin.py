"""Unit tests for the sso_admin module in aws_v2 package."""

import unittest
from unittest.mock import patch

from aws_v2.sso_admin import (
    AccountAssignmentCreationStatus,
    create_account_assignment,
)


class TestSSOAdmin(unittest.TestCase):

    def setUp(self):
        """Set up common test data for SSOAdmin tests."""
        self.mock_response = {
            "AccountAssignment": {
                "Status": "SUCCEEDED",
                "RequestId": "12345",
                "CreatedDate": "2025-08-24T12:00:00Z",
                "FailureReason": None,
            }
        }

    @patch("aws_v2.sso_admin.client")
    def test_create_account_assignment(self, mock_client):
        """Test create_account_assignment returns expected status."""
        mock_client.create_account_assignment.return_value = self.mock_response
        result = create_account_assignment(
            instance_arn="arn:aws:sso:::instance/sso-instance-id",
            permission_set_arn="arn:aws:sso:::permissionSet/permission-set-id",
            principal_id="principal-id",
            target_id="target-id",
            principal_type="USER",
            sso_admin_client=mock_client,
        )
        self.assertIsInstance(result, AccountAssignmentCreationStatus)
        self.assertEqual(result.status, "SUCCEEDED")
        self.assertEqual(result.request_id, "12345")
        self.assertEqual(result.created_date, "2025-08-24T12:00:00Z")
        self.assertIsNone(result.failure_reason)


if __name__ == "__main__":
    unittest.main()
