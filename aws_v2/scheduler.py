"""
This module provides utilities for interacting with AWS EventBridge Scheduler.
Includes functions for managing schedules and schedule groups.
"""

from typing import Dict, List, Optional

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.scheduler import (
    CreateScheduleGroupResponse,
    CreateScheduleResponse,
    FlexibleTimeWindow,
    ListScheduleGroupsResponse,
    ListSchedulesResponse,
    ListTagsForResourceResponse,
    Schedule,
    ScheduleGroup,
    ScheduleGroupSummary,
    ScheduleSummary,
    Tag,
    Target,
    UpdateScheduleResponse,
)

client = session.client("scheduler")


@pivot_exceptions
def create_schedule(
    name: str,
    schedule_expression: str,
    flexible_time_window: Dict,
    target: Dict,
    group_name: Optional[str] = None,
    description: Optional[str] = None,
    state: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    schedule_expression_timezone: Optional[str] = None,
    kms_key_arn: Optional[str] = None,
    action_after_completion: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> CreateScheduleResponse:
    """
    Creates a new EventBridge Scheduler schedule.

    Args:
        name (str): The name of the schedule.
        schedule_expression (str): The scheduling expression.
        flexible_time_window (Dict): Flexible time window config.
        target (Dict): Target configuration including ARN and role.
        group_name (str, optional): The name of the schedule group.
        description (str, optional): Description of the schedule.
        state (str, optional): State (ENABLED or DISABLED).
        start_date (str, optional): The date to start the schedule.
        end_date (str, optional): The date to end the schedule.
        schedule_expression_timezone (str, optional): Timezone.
        kms_key_arn (str, optional): KMS key ARN for encryption.
        action_after_completion (str, optional): Action after completion.
        scheduler_client (boto3.client, optional): Custom client.

    Returns:
        CreateScheduleResponse: Object containing the schedule ARN.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {
        "Name": name,
        "ScheduleExpression": schedule_expression,
        "FlexibleTimeWindow": flexible_time_window,
        "Target": target,
    }

    if group_name:
        params["GroupName"] = group_name
    if description:
        params["Description"] = description
    if state:
        params["State"] = state
    if start_date:
        params["StartDate"] = start_date
    if end_date:
        params["EndDate"] = end_date
    if schedule_expression_timezone:
        params["ScheduleExpressionTimezone"] = schedule_expression_timezone
    if kms_key_arn:
        params["KmsKeyArn"] = kms_key_arn
    if action_after_completion:
        params["ActionAfterCompletion"] = action_after_completion

    response = scheduler_client.create_schedule(**params)
    return CreateScheduleResponse(schedule_arn=response["ScheduleArn"])


@pivot_exceptions
def create_schedule_group(
    name: str,
    tags: Optional[List[Dict]] = None,
    scheduler_client: boto3.client = None,
) -> CreateScheduleGroupResponse:
    """
    Creates a new EventBridge Scheduler schedule group.

    Args:
        name (str): The name of the schedule group.
        tags (List[Dict], optional): Tags to assign to the schedule group.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        CreateScheduleGroupResponse: Object containing the schedule group ARN.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {"Name": name}
    if tags:
        params["Tags"] = tags

    response = scheduler_client.create_schedule_group(**params)
    return CreateScheduleGroupResponse(
        schedule_group_arn=response["ScheduleGroupArn"]
    )


@pivot_exceptions
def delete_schedule(
    name: str,
    group_name: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> None:
    """
    Deletes an EventBridge Scheduler schedule.

    Args:
        name (str): The name of the schedule to delete.
        group_name (str, optional): The name of the schedule group.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        None
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {"Name": name}
    if group_name:
        params["GroupName"] = group_name

    scheduler_client.delete_schedule(**params)


@pivot_exceptions
def delete_schedule_group(
    name: str, scheduler_client: boto3.client = None
) -> None:
    """
    Deletes an EventBridge Scheduler schedule group.

    Args:
        name (str): The name of the schedule group to delete.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        None
    """
    if scheduler_client is None:
        scheduler_client = client

    scheduler_client.delete_schedule_group(Name=name)


@pivot_exceptions
def get_schedule(
    name: str,
    group_name: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> Schedule:
    """
    Retrieves details about an EventBridge Scheduler schedule.

    Args:
        name (str): The name of the schedule.
        group_name (str, optional): The name of the schedule group.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        Schedule: Object containing the schedule details.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {"Name": name}
    if group_name:
        params["GroupName"] = group_name

    response = scheduler_client.get_schedule(**params)

    # Parse FlexibleTimeWindow
    ftw_data = response.get("FlexibleTimeWindow", {})
    flexible_time_window = FlexibleTimeWindow(
        mode=ftw_data.get("Mode"),
        maximum_window_in_minutes=ftw_data.get("MaximumWindowInMinutes"),
    )

    # Parse Target
    target_data = response.get("Target", {})
    target = Target(
        arn=target_data.get("Arn"),
        role_arn=target_data.get("RoleArn"),
        input=target_data.get("Input"),
        dead_letter_config=target_data.get("DeadLetterConfig"),
        retry_policy=target_data.get("RetryPolicy"),
    )

    return Schedule(
        name=response.get("Name"),
        arn=response.get("Arn"),
        group_name=response.get("GroupName"),
        schedule_expression=response.get("ScheduleExpression"),
        schedule_expression_timezone=response.get(
            "ScheduleExpressionTimezone"
        ),
        flexible_time_window=flexible_time_window,
        target=target,
        state=response.get("State"),
        description=response.get("Description"),
        start_date=response.get("StartDate"),
        end_date=response.get("EndDate"),
        creation_date=response.get("CreationDate"),
        last_modification_date=response.get("LastModificationDate"),
        kms_key_arn=response.get("KmsKeyArn"),
        action_after_completion=response.get("ActionAfterCompletion"),
    )


@pivot_exceptions
def get_schedule_group(
    name: str, scheduler_client: boto3.client = None
) -> ScheduleGroup:
    """
    Retrieves details about an EventBridge Scheduler schedule group.

    Args:
        name (str): The name of the schedule group.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        ScheduleGroup: Object containing the schedule group details.
    """
    if scheduler_client is None:
        scheduler_client = client

    response = scheduler_client.get_schedule_group(Name=name)

    return ScheduleGroup(
        name=response.get("Name"),
        arn=response.get("Arn"),
        state=response.get("State"),
        creation_date=response.get("CreationDate"),
        last_modification_date=response.get("LastModificationDate"),
    )


@pivot_exceptions
def list_schedule_groups(
    name_prefix: Optional[str] = None,
    max_results: Optional[int] = None,
    next_token: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> ListScheduleGroupsResponse:
    """
    Lists EventBridge Scheduler schedule groups.

    Args:
        name_prefix (str, optional): Prefix to filter schedule groups.
        max_results (int, optional): Maximum number of results to return.
        next_token (str, optional): Token for pagination.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        ListScheduleGroupsResponse: Object containing list of schedule groups.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {}
    if name_prefix:
        params["NamePrefix"] = name_prefix
    if max_results:
        params["MaxResults"] = max_results
    if next_token:
        params["NextToken"] = next_token

    response = scheduler_client.list_schedule_groups(**params)

    schedule_groups = []
    for group in response.get("ScheduleGroups", []):
        schedule_groups.append(
            ScheduleGroupSummary(
                name=group.get("Name"),
                arn=group.get("Arn"),
                state=group.get("State"),
                creation_date=group.get("CreationDate"),
                last_modification_date=group.get("LastModificationDate"),
            )
        )

    return ListScheduleGroupsResponse(
        schedule_groups=schedule_groups,
        next_token=response.get("NextToken"),
    )


@pivot_exceptions
def list_schedules(
    group_name: Optional[str] = None,
    name_prefix: Optional[str] = None,
    state: Optional[str] = None,
    max_results: Optional[int] = None,
    next_token: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> ListSchedulesResponse:
    """
    Lists EventBridge Scheduler schedules.

    Args:
        group_name (str, optional): Filter by schedule group name.
        name_prefix (str, optional): Prefix to filter schedules.
        state (str, optional): Filter by state (ENABLED or DISABLED).
        max_results (int, optional): Maximum number of results to return.
        next_token (str, optional): Token for pagination.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        ListSchedulesResponse: Object containing list of schedules.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {}
    if group_name:
        params["GroupName"] = group_name
    if name_prefix:
        params["NamePrefix"] = name_prefix
    if state:
        params["State"] = state
    if max_results:
        params["MaxResults"] = max_results
    if next_token:
        params["NextToken"] = next_token

    response = scheduler_client.list_schedules(**params)

    schedules = []
    for schedule in response.get("Schedules", []):
        schedules.append(
            ScheduleSummary(
                name=schedule.get("Name"),
                arn=schedule.get("Arn"),
                group_name=schedule.get("GroupName"),
                state=schedule.get("State"),
                target=schedule.get("Target"),
                creation_date=schedule.get("CreationDate"),
                last_modification_date=schedule.get("LastModificationDate"),
            )
        )

    return ListSchedulesResponse(
        schedules=schedules, next_token=response.get("NextToken")
    )


@pivot_exceptions
def list_tags_for_resource(
    resource_arn: str, scheduler_client: boto3.client = None
) -> ListTagsForResourceResponse:
    """
    Lists tags for an EventBridge Scheduler resource.

    Args:
        resource_arn (str): The ARN of the resource.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        ListTagsForResourceResponse: Object containing list of tags.
    """
    if scheduler_client is None:
        scheduler_client = client

    response = scheduler_client.list_tags_for_resource(
        ResourceArn=resource_arn
    )

    tags = []
    for tag in response.get("Tags", []):
        tags.append(Tag(key=tag.get("Key"), value=tag.get("Value")))

    return ListTagsForResourceResponse(tags=tags)


@pivot_exceptions
def tag_resource(
    resource_arn: str,
    tags: List[Dict],
    scheduler_client: boto3.client = None,
) -> None:
    """
    Adds tags to an EventBridge Scheduler resource.

    Args:
        resource_arn (str): The ARN of the resource.
        tags (List[Dict]): List of tags to add (each with Key and Value).
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        None
    """
    if scheduler_client is None:
        scheduler_client = client

    scheduler_client.tag_resource(ResourceArn=resource_arn, Tags=tags)


@pivot_exceptions
def untag_resource(
    resource_arn: str,
    tag_keys: List[str],
    scheduler_client: boto3.client = None,
) -> None:
    """
    Removes tags from an EventBridge Scheduler resource.

    Args:
        resource_arn (str): The ARN of the resource.
        tag_keys (List[str]): List of tag keys to remove.
        scheduler_client (boto3.client, optional): Custom scheduler client.

    Returns:
        None
    """
    if scheduler_client is None:
        scheduler_client = client

    scheduler_client.untag_resource(ResourceArn=resource_arn, TagKeys=tag_keys)


@pivot_exceptions
def update_schedule(
    name: str,
    schedule_expression: str,
    flexible_time_window: Dict,
    target: Dict,
    group_name: Optional[str] = None,
    description: Optional[str] = None,
    state: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    schedule_expression_timezone: Optional[str] = None,
    kms_key_arn: Optional[str] = None,
    action_after_completion: Optional[str] = None,
    scheduler_client: boto3.client = None,
) -> UpdateScheduleResponse:
    """
    Updates an existing EventBridge Scheduler schedule.

    Args:
        name (str): The name of the schedule.
        schedule_expression (str): The scheduling expression.
        flexible_time_window (Dict): Flexible time window config.
        target (Dict): Target configuration including ARN and role.
        group_name (str, optional): The name of the schedule group.
        description (str, optional): Description of the schedule.
        state (str, optional): State (ENABLED or DISABLED).
        start_date (str, optional): The date to start the schedule.
        end_date (str, optional): The date to end the schedule.
        schedule_expression_timezone (str, optional): Timezone.
        kms_key_arn (str, optional): KMS key ARN for encryption.
        action_after_completion (str, optional): Action after completion.
        scheduler_client (boto3.client, optional): Custom client.

    Returns:
        UpdateScheduleResponse: Object containing the schedule ARN.
    """
    if scheduler_client is None:
        scheduler_client = client

    params = {
        "Name": name,
        "ScheduleExpression": schedule_expression,
        "FlexibleTimeWindow": flexible_time_window,
        "Target": target,
    }

    if group_name:
        params["GroupName"] = group_name
    if description:
        params["Description"] = description
    if state:
        params["State"] = state
    if start_date:
        params["StartDate"] = start_date
    if end_date:
        params["EndDate"] = end_date
    if schedule_expression_timezone:
        params["ScheduleExpressionTimezone"] = schedule_expression_timezone
    if kms_key_arn:
        params["KmsKeyArn"] = kms_key_arn
    if action_after_completion:
        params["ActionAfterCompletion"] = action_after_completion

    response = scheduler_client.update_schedule(**params)
    return UpdateScheduleResponse(schedule_arn=response["ScheduleArn"])
