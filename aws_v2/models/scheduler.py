"""
Data models for AWS EventBridge Scheduler.
Contains dataclasses for EventBridge Scheduler API responses.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from .base import BaseModel


@dataclass
class Tag:
    """Represents a tag key-value pair."""

    key: str
    value: str


@dataclass
class FlexibleTimeWindow:
    """
    Represents the flexible time window for a schedule.
    Allows EventBridge Scheduler to invoke the target within a time window.
    """

    mode: str
    maximum_window_in_minutes: Optional[int] = None


@dataclass
class Target:
    """
    Represents the target for a schedule.
    Contains the ARN and role ARN for the target service.
    """

    arn: str
    role_arn: str
    input: Optional[str] = None
    dead_letter_config: Optional[Dict] = None
    retry_policy: Optional[Dict] = None


@dataclass
class Schedule(BaseModel):
    """
    Represents an EventBridge Scheduler schedule.
    Contains all schedule configuration and metadata.
    """

    name: str
    schedule_expression: str
    flexible_time_window: FlexibleTimeWindow
    target: Target
    arn: Optional[str] = None
    group_name: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    schedule_expression_timezone: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
    last_modification_date: Optional[datetime] = None
    kms_key_arn: Optional[str] = None
    action_after_completion: Optional[str] = None


@dataclass
class ScheduleGroup(BaseModel):
    """
    Represents an EventBridge Scheduler schedule group.
    Groups allow organizing and managing related schedules.
    """

    name: str
    arn: Optional[str] = None
    state: Optional[str] = None
    creation_date: Optional[datetime] = None
    last_modification_date: Optional[datetime] = None


@dataclass
class ScheduleSummary(BaseModel):
    """
    Represents a summary of a schedule for list operations.
    Contains basic schedule information without full details.
    """

    name: str
    arn: Optional[str] = None
    group_name: Optional[str] = None
    state: Optional[str] = None
    target: Optional[Dict] = None
    creation_date: Optional[datetime] = None
    last_modification_date: Optional[datetime] = None


@dataclass
class ScheduleGroupSummary(BaseModel):
    """
    Represents a summary of a schedule group for list operations.
    Contains basic group information without full details.
    """

    name: str
    arn: Optional[str] = None
    state: Optional[str] = None
    creation_date: Optional[datetime] = None
    last_modification_date: Optional[datetime] = None


@dataclass
class CreateScheduleResponse:
    """Response from create_schedule operation."""

    schedule_arn: str


@dataclass
class CreateScheduleGroupResponse:
    """Response from create_schedule_group operation."""

    schedule_group_arn: str


@dataclass
class UpdateScheduleResponse:
    """Response from update_schedule operation."""

    schedule_arn: str


@dataclass
class ListSchedulesResponse:
    """Response from list_schedules operation."""

    schedules: List[ScheduleSummary]
    next_token: Optional[str] = None


@dataclass
class ListScheduleGroupsResponse:
    """Response from list_schedule_groups operation."""

    schedule_groups: List[ScheduleGroupSummary]
    next_token: Optional[str] = None


@dataclass
class ListTagsForResourceResponse:
    """Response from list_tags_for_resource operation."""

    tags: List[Tag]
