# AWS v2 SDK Wrapper - AI Agent Guidelines

## Architecture Overview

This is a Python library providing an abstraction layer on top of boto3 for simplified AWS service interactions. Key architectural decisions:

- **Service Modules**: Each AWS service has a dedicated module in `aws_v2/` (e.g., `sts.py`, `s3.py`) with functions decorated with `@pivot_exceptions`
- **Unified Exception Handling**: All boto3 exceptions are transformed into `AwsError` exceptions via the `@pivot_exceptions` decorator
- **Role Chaining**: Built-in support for assuming IAM roles and creating new boto3 sessions with temporary credentials
- **Data Models**: Response objects are wrapped in dataclasses located in `aws_v2/models/` for type safety and consistency

## Core Patterns

### Service Module Structure
```python
# aws_v2/{service}.py
import boto3
from . import session
from .exceptions import pivot_exceptions
from .models.{service} import ResponseType

client = session.client("{service}")

@pivot_exceptions
def function_name(param: str, {service}_client: boto3.client = None) -> ResponseType:
    if {service}_client is None:
        {service}_client = client
    response = {service}_client.api_call(Param=param)
    return ResponseType(**response)
```

### Exception Handling
All service functions use `@pivot_exceptions` which transforms any boto3 exception into:
```python
raise AwsError(f"An error occurred in {func.__module__}.{func.__name__}: {exc}") from exc
```

### Role Assumption Workflow
```python
from aws_v2 import sts, get_session

# Assume role and get credentials
response = sts.assume_role(role_arn="arn:aws:iam::123456789012:role/MyRole")
# Create new session with assumed credentials
new_session = get_session(response.credentials, region_name="us-west-2")
# Use session to create service clients
s3_client = new_session.client("s3")
```

## Development Workflow

### Testing
- Use `unittest` framework with mocking of boto3 clients
- Tests located in `tests/` directory, one per service module
- Run tests: `uv run python -m unittest discover tests`

### Code Quality
- **Formatting**: `uv run black aws_v2 tests` (79 char line length)
- **Imports**: `uv run isort aws_v2 tests` (black profile)
- **Linting**: `uv run flake8 aws_v2 tests` (79 char limit, ignores E203, W503)

### Dependencies
- Managed with `uv` (Python 3.13+ required)
- Install: `uv install`
- Key dependencies: `boto3`, `black`, `isort`, `flake8`

## Key Files

- `aws_v2/__init__.py`: Global boto3 session setup and utility functions
- `aws_v2/exceptions.py`: `AwsError` class and `@pivot_exceptions` decorator
- `aws_v2/utils.py`: Role chaining utilities (`assume_role`, `get_client_with_role`)
- `aws_v2/models/base.py`: Common dataclasses (`CredentialsObject`, `Tag`)
- `pyproject.toml`: Project configuration, tool settings, and dependencies

## Conventions

- **Client Parameters**: All service functions accept optional `{service}_client` parameter for custom sessions
- **Region Handling**: Functions default to client's region if not specified
- **Data Models**: Use dataclasses with proper type hints, optional fields default to `None`
- **Imports**: Relative imports within the package, absolute for external dependencies
- **Documentation**: Module-level docstrings and function docstrings with Args/Returns sections</content>
<parameter name="filePath">/Users/rodenas/repos/aws_v2/.github/copilot-instructions.md