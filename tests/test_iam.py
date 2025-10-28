import unittest
from unittest.mock import MagicMock, patch

from aws_v2.iam import (
    Group,
    PolicyEntities,
    Role,
    User,
    list_entities_for_policy,
)


class TestIAM(unittest.TestCase):
    """
    Unit tests for the IAM module.
    """

    def setUp(self):
        """Set up common test data for IAM tests."""
        self.mock_policy_arn = "arn:aws:iam::123456789012:policy/TestPolicy"
        self.mock_groups = [
            {"GroupName": "Group1", "GroupId": "group1-id"},
            {"GroupName": "Group2", "GroupId": "group2-id"},
        ]
        self.mock_users = [
            {"UserName": "User1", "UserId": "user1-id"},
            {"UserName": "User2", "UserId": "user2-id"},
        ]
        self.mock_roles = [
            {"RoleName": "Role1", "RoleId": "role1-id"},
            {"RoleName": "Role2", "RoleId": "role2-id"},
        ]
        self.mock_paginator = MagicMock()
        self.mock_paginator.paginate.return_value = [
            {
                "PolicyGroups": self.mock_groups,
                "PolicyUsers": self.mock_users,
                "PolicyRoles": self.mock_roles,
            }
        ]

    @patch("aws_v2.iam.client")
    def test_list_entities_for_policy(self, mock_client):
        """Test list_entities_for_policy returns expected entities."""
        mock_client.get_paginator.return_value = self.mock_paginator
        result = list_entities_for_policy(
            self.mock_policy_arn, iam_client=mock_client
        )
        self.assertIsInstance(result, PolicyEntities)
        self.assertEqual(len(result.policy_groups), 2)
        self.assertEqual(len(result.policy_users), 2)
        self.assertEqual(len(result.policy_roles), 2)
        self.assertEqual(
            result.policy_groups[0],
            Group(group_name="Group1", group_id="group1-id"),
        )
        self.assertEqual(
            result.policy_users[0], User(user_name="User1", user_id="user1-id")
        )
        self.assertEqual(
            result.policy_roles[0], Role(role_name="Role1", role_id="role1-id")
        )


if __name__ == "__main__":
    unittest.main()
