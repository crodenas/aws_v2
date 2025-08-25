"""Unit tests for the identitystore module."""

import unittest
from unittest.mock import MagicMock, patch

from aws_v2.identitystore import Group, list_groups


class TestIdentityStore(unittest.TestCase):
    """
    Unit tests for the identitystore module.
    """

    def setUp(self):
        """Set up common test data for IdentityStore tests."""
        self.mock_identitystore_id = "d-0123456789"
        self.mock_groups = [
            {"GroupId": "group1", "DisplayName": "Group 1"},
            {"GroupId": "group2", "DisplayName": "Group 2"},
        ]
        self.mock_paginator = MagicMock()
        self.mock_paginator.paginate.return_value = [{"Groups": self.mock_groups}]

    @patch("aws_v2.identitystore.client")
    def test_list_groups(self, mock_client):
        """Test list_groups returns expected groups."""
        mock_client.get_paginator.return_value = self.mock_paginator
        result = list_groups(
            self.mock_identitystore_id, identitystore_client=mock_client
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], Group(group_id="group1", display_name="Group 1"))
        self.assertEqual(result[1], Group(group_id="group2", display_name="Group 2"))


if __name__ == "__main__":
    unittest.main()
