"""Unit tests for the cloudformation module in aws_v2 package."""

import unittest
from unittest.mock import patch

from aws_v2.cloudformation import create_stack, describe_stacks, list_stacks


class TestCloudFormation(unittest.TestCase):

    def setUp(self):
        """Set up common test data for CloudFormation tests."""
        self.stack_name = "test-stack"
        self.template_url = "https://example.com/template.yml"
        self.parameters = []
        self.capabilities = []

    @patch("aws_v2.cloudformation.client")
    def test_create_stack(self, mock_client):
        """Test create_stack returns expected stack info."""
        mock_response = {
            "StackId": "test-stack-id",
            "StackName": self.stack_name,
        }
        mock_client.create_stack.return_value = mock_response
        response = create_stack(
            self.stack_name,
            self.template_url,
            self.parameters,
            self.capabilities,
            mock_client,
        )
        self.assertEqual(response.stack_id, "test-stack-id")
        mock_client.create_stack.assert_called_once_with(
            StackName=self.stack_name,
            TemplateURL=self.template_url,
            Parameters=self.parameters,
            Capabilities=self.capabilities,
        )

    @patch("aws_v2.cloudformation.client")
    def test_describe_stacks(self, mock_client):
        """Test describe_stacks returns expected stack list."""
        mock_response = {
            "Stacks": [
                {
                    "StackId": "test-stack-id",
                    "StackName": "test-stack",
                    "Description": "Test stack",
                    "Parameters": [],
                    "Outputs": [],
                }
            ]
        }
        mock_client.get_paginator.return_value.paginate.return_value = [mock_response]
        response = describe_stacks(self.stack_name, mock_client)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].stack_id, "test-stack-id")
        self.assertEqual(response[0].stack_name, "test-stack")
        self.assertEqual(response[0].description, "Test stack")
        self.assertEqual(response[0].parameters, [])
        self.assertEqual(response[0].outputs, [])

    @patch("aws_v2.cloudformation.client")
    def test_list_stacks(self, mock_client):
        """Test list_stacks returns expected stack summaries."""
        mock_response = {
            "StackSummaries": [
                {
                    "StackId": "test-stack-id",
                    "StackName": "test-stack",
                }
            ]
        }
        mock_client.get_paginator.return_value.paginate.return_value = [mock_response]
        response = list_stacks("CREATE_COMPLETE", mock_client)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].stack_id, "test-stack-id")
        self.assertEqual(response[0].stack_name, "test-stack")


if __name__ == "__main__":
    unittest.main()
