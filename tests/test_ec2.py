"""Unit tests for EC2 utility functions."""

import unittest
from unittest.mock import MagicMock

from aws_v2.ec2 import describe_security_groups


class TestEC2(unittest.TestCase):
    """Test cases for EC2 utility functions."""

    def test_describe_security_groups(self):
        """Test the describe_security_groups function."""
        # Create mock EC2 client
        mock_ec2 = MagicMock()
        mock_paginator = MagicMock()
        mock_ec2.get_paginator.return_value = mock_paginator

        # Set up the mock paginator to return sample security groups
        mock_paginator.paginate.return_value = [
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

        # Call the function with the mock EC2 client
        result = describe_security_groups(mock_ec2)

        # Verify the results
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].GroupId, "sg-12345")
        self.assertEqual(result[0].GroupName, "default")
        self.assertEqual(result[0].Description, "default VPC security group")
        self.assertEqual(result[0].VpcId, "vpc-12345")

        self.assertEqual(result[1].GroupId, "sg-67890")
        self.assertEqual(result[1].GroupName, "web-servers")

        self.assertEqual(result[2].GroupId, "sg-abcde")
        self.assertEqual(result[2].GroupName, "db-servers")
        self.assertEqual(result[2].Description, "Security group for database servers")
        self.assertEqual(result[2].VpcId, "vpc-67890")

        # Verify the paginator was used correctly
        mock_ec2.get_paginator.assert_called_once_with("describe_security_groups")
        mock_paginator.paginate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
