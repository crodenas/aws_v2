"""Unit tests for EventBridge Scheduler utility functions."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from aws_v2.scheduler import (
    create_schedule,
    create_schedule_group,
    delete_schedule,
    delete_schedule_group,
    get_schedule,
    get_schedule_group,
    list_schedule_groups,
    list_schedules,
    list_tags_for_resource,
    tag_resource,
    untag_resource,
    update_schedule,
)


class TestScheduler(unittest.TestCase):
    """Test cases for EventBridge Scheduler utility functions."""

    def setUp(self):
        """Set up common test data for Scheduler tests."""
        self.mock_scheduler = MagicMock()

    @patch("aws_v2.scheduler.client")
    def test_create_schedule(self, mock_client):
        """Test create_schedule returns expected response."""
        mock_response = {
            "ScheduleArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            )
        }
        mock_client.create_schedule.return_value = mock_response

        flexible_time_window = {"Mode": "OFF"}
        target = {
            "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
            "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        }

        result = create_schedule(
            name="test-schedule",
            schedule_expression="rate(1 hour)",
            flexible_time_window=flexible_time_window,
            target=target,
            scheduler_client=mock_client,
        )

        self.assertEqual(
            result.schedule_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            ),
        )
        mock_client.create_schedule.assert_called_once()

    @patch("aws_v2.scheduler.client")
    def test_create_schedule_with_optional_params(self, mock_client):
        """Test create_schedule with optional parameters."""
        mock_response = {
            "ScheduleArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/my-group/test-schedule"
            )
        }
        mock_client.create_schedule.return_value = mock_response

        flexible_time_window = {
            "Mode": "FLEXIBLE",
            "MaximumWindowInMinutes": 15,
        }
        target = {
            "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
            "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        }

        result = create_schedule(
            name="test-schedule",
            schedule_expression="rate(1 hour)",
            flexible_time_window=flexible_time_window,
            target=target,
            group_name="my-group",
            description="Test schedule",
            state="ENABLED",
            scheduler_client=mock_client,
        )

        self.assertEqual(
            result.schedule_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/my-group/test-schedule"
            ),
        )
        call_args = mock_client.create_schedule.call_args[1]
        self.assertEqual(call_args["GroupName"], "my-group")
        self.assertEqual(call_args["Description"], "Test schedule")
        self.assertEqual(call_args["State"], "ENABLED")

    @patch("aws_v2.scheduler.client")
    def test_create_schedule_group(self, mock_client):
        """Test create_schedule_group returns expected response."""
        mock_response = {
            "ScheduleGroupArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            )
        }
        mock_client.create_schedule_group.return_value = mock_response

        result = create_schedule_group(
            name="test-group", scheduler_client=mock_client
        )

        self.assertEqual(
            result.schedule_group_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
        )
        mock_client.create_schedule_group.assert_called_once_with(
            Name="test-group"
        )

    @patch("aws_v2.scheduler.client")
    def test_create_schedule_group_with_tags(self, mock_client):
        """Test create_schedule_group with tags."""
        mock_response = {
            "ScheduleGroupArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            )
        }
        mock_client.create_schedule_group.return_value = mock_response

        tags = [{"Key": "Environment", "Value": "Test"}]
        result = create_schedule_group(
            name="test-group", tags=tags, scheduler_client=mock_client
        )

        self.assertEqual(
            result.schedule_group_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
        )
        call_args = mock_client.create_schedule_group.call_args[1]
        self.assertEqual(call_args["Tags"], tags)

    @patch("aws_v2.scheduler.client")
    def test_delete_schedule(self, mock_client):
        """Test delete_schedule calls the API correctly."""
        mock_client.delete_schedule.return_value = {}

        delete_schedule(name="test-schedule", scheduler_client=mock_client)

        mock_client.delete_schedule.assert_called_once_with(
            Name="test-schedule"
        )

    @patch("aws_v2.scheduler.client")
    def test_delete_schedule_with_group(self, mock_client):
        """Test delete_schedule with group_name."""
        mock_client.delete_schedule.return_value = {}

        delete_schedule(
            name="test-schedule",
            group_name="my-group",
            scheduler_client=mock_client,
        )

        mock_client.delete_schedule.assert_called_once_with(
            Name="test-schedule", GroupName="my-group"
        )

    @patch("aws_v2.scheduler.client")
    def test_delete_schedule_group(self, mock_client):
        """Test delete_schedule_group calls the API correctly."""
        mock_client.delete_schedule_group.return_value = {}

        delete_schedule_group(name="test-group", scheduler_client=mock_client)

        mock_client.delete_schedule_group.assert_called_once_with(
            Name="test-group"
        )

    @patch("aws_v2.scheduler.client")
    def test_get_schedule(self, mock_client):
        """Test get_schedule returns expected schedule details."""
        mock_response = {
            "Name": "test-schedule",
            "Arn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            ),
            "GroupName": "default",
            "ScheduleExpression": "rate(1 hour)",
            "ScheduleExpressionTimezone": "UTC",
            "State": "ENABLED",
            "Description": "Test schedule",
            "FlexibleTimeWindow": {"Mode": "OFF"},
            "Target": {
                "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
                "RoleArn": "arn:aws:iam::123456789012:role/test-role",
            },
            "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
            "LastModificationDate": datetime(2025, 1, 2, 12, 0, 0),
        }
        mock_client.get_schedule.return_value = mock_response

        result = get_schedule(
            name="test-schedule", scheduler_client=mock_client
        )

        self.assertEqual(result.name, "test-schedule")
        self.assertEqual(result.schedule_expression, "rate(1 hour)")
        self.assertEqual(result.state, "ENABLED")
        self.assertEqual(result.flexible_time_window.mode, "OFF")
        self.assertEqual(
            result.target.arn,
            "arn:aws:lambda:us-east-1:123456789012:function:test",
        )
        mock_client.get_schedule.assert_called_once_with(Name="test-schedule")

    @patch("aws_v2.scheduler.client")
    def test_get_schedule_with_group(self, mock_client):
        """Test get_schedule with group_name."""
        mock_response = {
            "Name": "test-schedule",
            "Arn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/my-group/test-schedule"
            ),
            "GroupName": "my-group",
            "ScheduleExpression": "rate(1 hour)",
            "FlexibleTimeWindow": {"Mode": "OFF"},
            "Target": {
                "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
                "RoleArn": "arn:aws:iam::123456789012:role/test-role",
            },
        }
        mock_client.get_schedule.return_value = mock_response

        result = get_schedule(
            name="test-schedule",
            group_name="my-group",
            scheduler_client=mock_client,
        )

        self.assertEqual(result.group_name, "my-group")
        mock_client.get_schedule.assert_called_once_with(
            Name="test-schedule", GroupName="my-group"
        )

    @patch("aws_v2.scheduler.client")
    def test_get_schedule_group(self, mock_client):
        """Test get_schedule_group returns expected group details."""
        mock_response = {
            "Name": "test-group",
            "Arn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            "State": "ACTIVE",
            "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
            "LastModificationDate": datetime(2025, 1, 2, 12, 0, 0),
        }
        mock_client.get_schedule_group.return_value = mock_response

        result = get_schedule_group(
            name="test-group", scheduler_client=mock_client
        )

        self.assertEqual(result.name, "test-group")
        self.assertEqual(result.state, "ACTIVE")
        self.assertEqual(
            result.arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
        )
        mock_client.get_schedule_group.assert_called_once_with(
            Name="test-group"
        )

    @patch("aws_v2.scheduler.client")
    def test_list_schedule_groups(self, mock_client):
        """Test list_schedule_groups returns list of groups."""
        mock_response = {
            "ScheduleGroups": [
                {
                    "Name": "group-1",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule-group/group-1"
                    ),
                    "State": "ACTIVE",
                    "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
                },
                {
                    "Name": "group-2",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule-group/group-2"
                    ),
                    "State": "ACTIVE",
                    "CreationDate": datetime(2025, 1, 2, 12, 0, 0),
                },
            ]
        }
        mock_client.list_schedule_groups.return_value = mock_response

        result = list_schedule_groups(scheduler_client=mock_client)

        self.assertEqual(len(result.schedule_groups), 2)
        self.assertEqual(result.schedule_groups[0].name, "group-1")
        self.assertEqual(result.schedule_groups[1].name, "group-2")
        mock_client.list_schedule_groups.assert_called_once_with()

    @patch("aws_v2.scheduler.client")
    def test_list_schedule_groups_with_params(self, mock_client):
        """Test list_schedule_groups with optional parameters."""
        mock_response = {
            "ScheduleGroups": [
                {
                    "Name": "test-group-1",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule-group/test-group-1"
                    ),
                    "State": "ACTIVE",
                }
            ],
            "NextToken": "next-token-123",
        }
        mock_client.list_schedule_groups.return_value = mock_response

        result = list_schedule_groups(
            name_prefix="test-",
            max_results=10,
            next_token="token-123",
            scheduler_client=mock_client,
        )

        self.assertEqual(len(result.schedule_groups), 1)
        self.assertEqual(result.next_token, "next-token-123")
        call_args = mock_client.list_schedule_groups.call_args[1]
        self.assertEqual(call_args["NamePrefix"], "test-")
        self.assertEqual(call_args["MaxResults"], 10)
        self.assertEqual(call_args["NextToken"], "token-123")

    @patch("aws_v2.scheduler.client")
    def test_list_schedules(self, mock_client):
        """Test list_schedules returns list of schedules."""
        mock_response = {
            "Schedules": [
                {
                    "Name": "schedule-1",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule/default/schedule-1"
                    ),
                    "GroupName": "default",
                    "State": "ENABLED",
                    "CreationDate": datetime(2025, 1, 1, 12, 0, 0),
                },
                {
                    "Name": "schedule-2",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule/default/schedule-2"
                    ),
                    "GroupName": "default",
                    "State": "DISABLED",
                    "CreationDate": datetime(2025, 1, 2, 12, 0, 0),
                },
            ]
        }
        mock_client.list_schedules.return_value = mock_response

        result = list_schedules(scheduler_client=mock_client)

        self.assertEqual(len(result.schedules), 2)
        self.assertEqual(result.schedules[0].name, "schedule-1")
        self.assertEqual(result.schedules[0].state, "ENABLED")
        self.assertEqual(result.schedules[1].name, "schedule-2")
        self.assertEqual(result.schedules[1].state, "DISABLED")
        mock_client.list_schedules.assert_called_once_with()

    @patch("aws_v2.scheduler.client")
    def test_list_schedules_with_params(self, mock_client):
        """Test list_schedules with optional parameters."""
        mock_response = {
            "Schedules": [
                {
                    "Name": "test-schedule-1",
                    "Arn": (
                        "arn:aws:scheduler:us-east-1:123456789012:"
                        "schedule/my-group/test-schedule-1"
                    ),
                    "GroupName": "my-group",
                    "State": "ENABLED",
                }
            ],
            "NextToken": "next-token-456",
        }
        mock_client.list_schedules.return_value = mock_response

        result = list_schedules(
            group_name="my-group",
            name_prefix="test-",
            state="ENABLED",
            max_results=20,
            next_token="token-456",
            scheduler_client=mock_client,
        )

        self.assertEqual(len(result.schedules), 1)
        self.assertEqual(result.next_token, "next-token-456")
        call_args = mock_client.list_schedules.call_args[1]
        self.assertEqual(call_args["GroupName"], "my-group")
        self.assertEqual(call_args["NamePrefix"], "test-")
        self.assertEqual(call_args["State"], "ENABLED")
        self.assertEqual(call_args["MaxResults"], 20)
        self.assertEqual(call_args["NextToken"], "token-456")

    @patch("aws_v2.scheduler.client")
    def test_list_tags_for_resource(self, mock_client):
        """Test list_tags_for_resource returns list of tags."""
        mock_response = {
            "Tags": [
                {"Key": "Environment", "Value": "Test"},
                {"Key": "Owner", "Value": "TeamA"},
            ]
        }
        mock_client.list_tags_for_resource.return_value = mock_response

        result = list_tags_for_resource(
            resource_arn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            scheduler_client=mock_client,
        )

        self.assertEqual(len(result.tags), 2)
        self.assertEqual(result.tags[0].key, "Environment")
        self.assertEqual(result.tags[0].value, "Test")
        self.assertEqual(result.tags[1].key, "Owner")
        self.assertEqual(result.tags[1].value, "TeamA")
        mock_client.list_tags_for_resource.assert_called_once_with(
            ResourceArn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            )
        )

    @patch("aws_v2.scheduler.client")
    def test_tag_resource(self, mock_client):
        """Test tag_resource calls the API correctly."""
        mock_client.tag_resource.return_value = {}

        tags = [{"Key": "Environment", "Value": "Production"}]
        tag_resource(
            resource_arn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            tags=tags,
            scheduler_client=mock_client,
        )

        mock_client.tag_resource.assert_called_once_with(
            ResourceArn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            Tags=tags,
        )

    @patch("aws_v2.scheduler.client")
    def test_untag_resource(self, mock_client):
        """Test untag_resource calls the API correctly."""
        mock_client.untag_resource.return_value = {}

        tag_keys = ["Environment", "Owner"]
        untag_resource(
            resource_arn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            tag_keys=tag_keys,
            scheduler_client=mock_client,
        )

        mock_client.untag_resource.assert_called_once_with(
            ResourceArn=(
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule-group/test-group"
            ),
            TagKeys=tag_keys,
        )

    @patch("aws_v2.scheduler.client")
    def test_update_schedule(self, mock_client):
        """Test update_schedule returns expected response."""
        mock_response = {
            "ScheduleArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            )
        }
        mock_client.update_schedule.return_value = mock_response

        flexible_time_window = {"Mode": "OFF"}
        target = {
            "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
            "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        }

        result = update_schedule(
            name="test-schedule",
            schedule_expression="rate(2 hours)",
            flexible_time_window=flexible_time_window,
            target=target,
            scheduler_client=mock_client,
        )

        self.assertEqual(
            result.schedule_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            ),
        )
        mock_client.update_schedule.assert_called_once()

    @patch("aws_v2.scheduler.client")
    def test_update_schedule_with_optional_params(self, mock_client):
        """Test update_schedule with optional parameters."""
        mock_response = {
            "ScheduleArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/my-group/test-schedule"
            )
        }
        mock_client.update_schedule.return_value = mock_response

        flexible_time_window = {
            "Mode": "FLEXIBLE",
            "MaximumWindowInMinutes": 30,
        }
        target = {
            "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
            "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        }

        result = update_schedule(
            name="test-schedule",
            schedule_expression="rate(2 hours)",
            flexible_time_window=flexible_time_window,
            target=target,
            group_name="my-group",
            description="Updated schedule",
            state="DISABLED",
            scheduler_client=mock_client,
        )

        self.assertEqual(
            result.schedule_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/my-group/test-schedule"
            ),
        )
        call_args = mock_client.update_schedule.call_args[1]
        self.assertEqual(call_args["GroupName"], "my-group")
        self.assertEqual(call_args["Description"], "Updated schedule")
        self.assertEqual(call_args["State"], "DISABLED")

    @patch("aws_v2.scheduler.client")
    def test_create_schedule_with_default_client(self, mock_client):
        """Test create_schedule with the default client."""
        mock_response = {
            "ScheduleArn": (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            )
        }
        mock_client.create_schedule.return_value = mock_response

        flexible_time_window = {"Mode": "OFF"}
        target = {
            "Arn": "arn:aws:lambda:us-east-1:123456789012:function:test",
            "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        }

        result = create_schedule(
            name="test-schedule",
            schedule_expression="rate(1 hour)",
            flexible_time_window=flexible_time_window,
            target=target,
        )

        self.assertEqual(
            result.schedule_arn,
            (
                "arn:aws:scheduler:us-east-1:123456789012:"
                "schedule/default/test-schedule"
            ),
        )


if __name__ == "__main__":
    unittest.main()
