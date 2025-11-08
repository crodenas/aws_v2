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
- **Documentation**: Module-level docstrings and function docstrings with Args/Returns sections

## Testing Patterns

### Test Structure
Each test file should follow this pattern:
```python
import unittest
from unittest.mock import MagicMock, patch

from aws_v2.{service} import function_to_test

class Test{Service}(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.mock_client = MagicMock()
        # Setup mock responses
    
    @patch("aws_v2.{service}.client")
    def test_function_name(self, mock_client):
        """Test function returns expected result."""
        mock_client.api_call.return_value = {"Key": "Value"}
        result = function_to_test(param="value")
        self.assertEqual(result.key, "Value")
```

### Mocking Guidelines
- Mock boto3 clients using `@patch("aws_v2.{service}.client")`
- Use `MagicMock()` for custom client instances
- Mock paginators when testing list operations with pagination
- Always test both success and error cases

## Security Considerations

- **Credentials Management**: Never hardcode AWS credentials. Always use boto3 session/environment variables
- **Role ARNs**: Validate role ARN format before passing to assume_role functions
- **Session Tokens**: Temporary credentials from `assume_role` include session tokens that expire
- **Error Messages**: The `AwsError` exception may include sensitive information from boto3 exceptions. Handle carefully in logs
- **Client Injection**: The optional `{service}_client` parameter allows custom sessions but should only accept trusted client instances

## Common Pitfalls

### Region Configuration
❌ **Wrong**: Assuming default region is set
```python
# This may fail if AWS_REGION is not configured
client = session.client("s3")
```

✅ **Correct**: Handle region explicitly or check session region
```python
# Use region_name parameter or verify session.region_name exists
if session.region_name is None:
    session = boto3.session.Session(region_name="us-east-2")
```

### Exception Handling
❌ **Wrong**: Catching specific boto3 exceptions
```python
try:
    result = s3.list_buckets()
except ClientError as e:  # Won't catch - exceptions are transformed
    handle_error(e)
```

✅ **Correct**: Catch AwsError instead
```python
from aws_v2.exceptions import AwsError

try:
    result = s3.list_buckets()
except AwsError as e:
    handle_error(e)
```

### Client Parameter Pattern
❌ **Wrong**: Not defaulting to module client
```python
def my_function(param: str, s3_client: boto3.client) -> Response:
    # Forces caller to always provide client
    return s3_client.get_object(Bucket=param)
```

✅ **Correct**: Default to module-level client
```python
def my_function(param: str, s3_client: boto3.client = None) -> Response:
    if s3_client is None:
        s3_client = client  # Use module-level client
    return s3_client.get_object(Bucket=param)
```

### Role Chaining
❌ **Wrong**: Creating new sessions without using wrapper utilities
```python
# Bypasses exception handling and role chaining utilities
response = boto3.client("sts").assume_role(RoleArn=role_arn)
credentials = response["Credentials"]
new_session = boto3.Session(
    aws_access_key_id=credentials["AccessKeyId"],
    # ... manual credential mapping
)
```

✅ **Correct**: Use provided utilities
```python
from aws_v2 import sts, get_session

# Uses proper exception handling and credential mapping
response = sts.assume_role(role_arn=role_arn)
new_session = get_session(response.credentials, region_name="us-west-2")
```

## Adding New Service Modules

When adding support for a new AWS service:

1. **Create service module**: `aws_v2/{service}.py`
2. **Define models**: Add response dataclasses in `aws_v2/models/{service}.py`
3. **Follow the pattern**:
   - Import required dependencies
   - Create module-level client: `client = session.client("{service}")`
   - Decorate all functions with `@pivot_exceptions`
   - Accept optional `{service}_client` parameter
   - Return dataclass instances, not raw boto3 responses
4. **Add tests**: Create `tests/test_{service}.py` with unittest cases
5. **Update documentation**: Add service to README.md service list
<parameter name="filePath">/Users/rodenas/repos/aws_v2/.github/copilot-instructions.md