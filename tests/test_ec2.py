"""Unit tests for EC2 utility functions."""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.ec2 import describe_security_groups


class TestEC2(unittest.TestCase):
    """Test cases for EC2 utility functions."""

    def setUp(self):
        """Set up common test data for EC2 tests."""
        self.mock_ec2 = MagicMock()
        self.mock_paginator = MagicMock()
        self.mock_ec2.get_paginator.return_value = self.mock_paginator
        self.mock_paginator.paginate.return_value = [
            {
                "SecurityGroups": [
                    {
                        "GroupId": "sg-12345",
                        "GroupName": "default",
                        "Description": "default VPC security group",
                        "VpcId": "vpc-12345",
                    },
                    {
                        "GroupId": "sg-67890",
                        "GroupName": "web-servers",
                        "Description": "Security group for web servers",
                        "VpcId": "vpc-12345",
                    },
                ]
            },
            {
                "SecurityGroups": [
                    {
                        "GroupId": "sg-abcde",
                        "GroupName": "db-servers",
                        "Description": "Security group for database servers",
                        "VpcId": "vpc-67890",
                    }
                ]
            },
        ]

    @patch("aws_v2.ec2.client")
    def test_describe_security_groups(self, mock_client):
        """Test describe_security_groups returns expected security groups."""
        mock_client.get_paginator.return_value = self.mock_paginator
        result = describe_security_groups(mock_client)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].group_id, "sg-12345")
        self.assertEqual(result[0].group_name, "default")
        self.assertEqual(result[0].description, "default VPC security group")
        self.assertEqual(result[0].vpc_id, "vpc-12345")
        self.assertEqual(result[1].group_id, "sg-67890")
        self.assertEqual(result[1].group_name, "web-servers")

        self.assertEqual(result[2].group_id, "sg-abcde")
        self.assertEqual(result[2].group_name, "db-servers")
        self.assertEqual(result[2].description, "Security group for database servers")
        self.assertEqual(result[2].vpc_id, "vpc-67890")

        # Verify the paginator was used correctly
        mock_client.get_paginator.assert_called_once_with("describe_security_groups")
        self.mock_paginator.paginate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
