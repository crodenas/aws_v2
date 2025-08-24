import unittest
from unittest.mock import MagicMock, patch

from aws_v2.iam import list_entities_for_policy, Group, User, Role, PolicyEntities


class TestIAM(unittest.TestCase):
    """
    Unit tests for the IAM module.
    """

    @patch("aws_v2.iam.client")
    def test_list_entities_for_policy(self, mock_client):
        """
        Test the list_entities_for_policy function.
        """
        # Mock data
        mock_policy_arn = "arn:aws:iam::123456789012:policy/TestPolicy"
        mock_groups = [
            {"GroupName": "Group1", "GroupId": "group1-id"},
            {"GroupName": "Group2", "GroupId": "group2-id"},
        ]
        mock_users = [
            {"UserName": "User1", "UserId": "user1-id"},
            {"UserName": "User2", "UserId": "user2-id"},
        ]
        mock_roles = [
            {"RoleName": "Role1", "RoleId": "role1-id"},
            {"RoleName": "Role2", "RoleId": "role2-id"},
        ]

        # Mock paginator
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {
                "PolicyGroups": mock_groups,
                "PolicyUsers": mock_users,
                "PolicyRoles": mock_roles,
            }
        ]
        mock_client.get_paginator.return_value = mock_paginator

        # Call the function
        result = list_entities_for_policy(mock_policy_arn, iam_client=mock_client)

        # Assertions
        self.assertIsInstance(result, PolicyEntities)
        self.assertEqual(len(result.policy_groups), 2)
        self.assertEqual(len(result.policy_users), 2)
        self.assertEqual(len(result.policy_roles), 2)

        self.assertEqual(
            result.policy_groups[0], Group(group_name="Group1", group_id="group1-id")
        )
        self.assertEqual(
            result.policy_users[0], User(user_name="User1", user_id="user1-id")
        )
        self.assertEqual(
            result.policy_roles[0], Role(role_name="Role1", role_id="role1-id")
        )


if __name__ == "__main__":
    unittest.main()
