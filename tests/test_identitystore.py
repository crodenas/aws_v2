"""
Unit tests for the identitystore module.
"""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.identitystore import Group, list_groups


class TestIdentityStore(unittest.TestCase):
    """
    Unit tests for the identitystore module.
    """

    @patch("aws_v2.identitystore.client")
    def test_list_groups(self, mock_client):
        """
        Test the list_groups function.
        """
        # Mock data
        mock_identitystore_id = "d-0123456789"
        mock_groups = [
            {"GroupId": "group1", "DisplayName": "Group 1"},
            {"GroupId": "group2", "DisplayName": "Group 2"},
        ]

        # Mock paginator
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"Groups": mock_groups}]
        mock_client.get_paginator.return_value = mock_paginator

        # Call the function
        result = list_groups(mock_identitystore_id, identitystore_client=mock_client)

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], Group(GroupId="group1", DisplayName="Group 1"))
        self.assertEqual(result[1], Group(GroupId="group2", DisplayName="Group 2"))


if __name__ == "__main__":
    unittest.main()
