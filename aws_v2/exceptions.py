"""
Exception handling utilities for AWS operations.

This module provides the AwsError exception class and the pivot_exceptions
decorator for transforming boto3 exceptions into local exceptions.
"""

import functools


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
        except Exception as exc:
            raise AwsError(
                f"An error occurred in "
                f"{func.__module__}.{func.__name__}: {exc}"
            ) from exc

    return wrapper
