"module"

import functools


class AwsError(Exception):
    "class"


def pivot_exceptions(func):
    "decorator"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            raise AwsError(
                f"An error occurred in {func.__module__}.{func.__name__}: {exc}"
            ) from exc

    return wrapper
