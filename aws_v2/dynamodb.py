"""
DynamoDB module for AWS operations.

This module provides functions for interacting with AWS DynamoDB service,
including operations like scanning tables, querying data, etc.
"""

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.dynamodb import DynamoDBScanOutput

client = session.client("dynamodb")


@pivot_exceptions
def scan(
    table_name: str,
    filter_expression: str = None,
    expression_attr_val: dict = None,
    dynamodb_client: boto3.client = None,
) -> DynamoDBScanOutput:
    """
    Scan a DynamoDB table with optional filtering.

    This function performs a complete scan of a DynamoDB table, handling pagination
    automatically to retrieve all items that match the provided filter expression.

    Args:
        table_name (str): The name of the DynamoDB table to scan.
        filter_expression (str, optional): A filter expression for the scan operation.
            Defaults to None.
        expression_attr_val (dict, optional): A dictionary of expression attribute values
            for the filter expression. Defaults to None.
        dynamodb_client (boto3.client, optional): A boto3 DynamoDB client to use for the operation.
            If None, the default client will be used. Defaults to None.

    Returns:
        DynamoDBScanOutput: An object containing the scan results, including items, count,
                           scanned count, and other metadata.

    Examples:
        >>> scan("my-table")
        DynamoDBScanOutput(items=[...], count=10, scanned_count=10, ...)

        >>> scan(
        ...     "my-table",
        ...     filter_expression="attribute = :value",
        ...     expression_attr_val={":value": {"S": "example"}}
        ... )
        DynamoDBScanOutput(items=[...], count=5, scanned_count=10, ...)
    """

    if dynamodb_client is None:
        dynamodb_client = client

    items = []
    responses = []
    last_evaluated_key = None

    while True:
        if filter_expression:
            scan_kwargs = {
                "TableName": table_name,
                "FilterExpression": filter_expression,
                "ExpressionAttributeValues": expression_attr_val,
            }
        else:
            scan_kwargs = {"TableName": table_name}

        if last_evaluated_key:
            scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = dynamodb_client.scan(**scan_kwargs)
        responses.append(response)
        items.extend(response.get("Items", []))

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return DynamoDBScanOutput(
        items=items,
        count=sum(resp.get("Count", 0) for resp in responses),
        scanned_count=sum(resp.get("ScannedCount", 0) for resp in responses),
        last_evaluated_key=last_evaluated_key,
        consumed_capacity=response.get("ConsumedCapacity"),
    )
