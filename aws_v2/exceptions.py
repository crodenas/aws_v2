"""
Exception handling utilities for AWS operations.

This module provides the AwsError exception class and the pivot_exceptions
decorator for transforming boto3 exceptions into local exceptions.
"""

import functools
from botocore.exceptions import ClientError


class AwsError(Exception):
    """
    Custom exception for AWS operations.

    All boto3 exceptions are transformed into this exception type
    for unified error handling across the library.
    """


def pivot_exceptions(func):
    """
    Decorator that transforms any exception into an AwsError.

    This decorator wraps service functions to catch all exceptions
    and convert them into AwsError instances with context about
    where the error occurred.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function that raises AwsError on any exception.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as client_exc:
            if (
                client_exc.response["Error"]["Code"]
                == "UnrecognizedClientException"
            ):
                raise AwsError(
                    "AWS credentials are not configured or invalid. "
                    "Please run 'aws configure' or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
                ) from client_exc
            raise AwsError(
                f"An error occurred in "
                f"{func.__module__}.{func.__name__}: {client_exc}"
            ) from client_exc
        except Exception as exc:
            raise AwsError(
                f"An error occurred in "
                f"{func.__module__}.{func.__name__}: {exc}"
            ) from exc

    return wrapper
