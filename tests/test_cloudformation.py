import unittest
from unittest.mock import patch

from aws_v2.cloudformation import create_stack, describe_stacks, list_stacks


class TestCloudFormation(unittest.TestCase):

    @patch("aws_v2.cloudformation.client")
    def test_create_stack(self, mock_client):
        mock_response = {"StackId": "test-stack-id", "StackName": "test-stack"}
        mock_client.create_stack.return_value = mock_response

        stack_name = "test-stack"
        template_url = "https://example.com/template.yml"
        parameters = []
        capabilities = []

        response = create_stack(
            stack_name, template_url, parameters, capabilities, mock_client
        )

        self.assertEqual(response.stack_id, "test-stack-id")
        self.assertEqual(response.stack_name, "test-stack")
        mock_client.create_stack.assert_called_once_with(
            StackName=stack_name,
            TemplateURL=template_url,
            Parameters=parameters,
            Capabilities=capabilities,
        )

    @patch("aws_v2.cloudformation.client")
    def test_describe_stacks(self, mock_client):
        mock_response = {
            "Stacks": [{"StackId": "test-stack-id", "StackName": "test-stack"}]
        }
        mock_client.get_paginator.return_value.paginate.return_value = [mock_response]

        response = describe_stacks("test-stack", mock_client)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].stack_id, "test-stack-id")
        self.assertEqual(response[0].stack_name, "test-stack")

    @patch("aws_v2.cloudformation.client")
    def test_list_stacks(self, mock_client):
        mock_response = {
            "StackSummaries": [{"StackId": "test-stack-id", "StackName": "test-stack"}]
        }
        mock_client.get_paginator.return_value.paginate.return_value = [mock_response]

        response = list_stacks("CREATE_COMPLETE", mock_client)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].stack_id, "test-stack-id")
        self.assertEqual(response[0].stack_name, "test-stack")


if __name__ == "__main__":
    unittest.main()
