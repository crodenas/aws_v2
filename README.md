# AWS v2 SDK Wrapper

A Python library providing an abstraction layer on top of boto3 for simplified AWS service interactions, with built-in role chaining and unified exception handling.

## Purpose

This library is designed as an abstraction on top of boto3 to allow easy proper role chaining. By using the service modules implemented here, it also transforms all boto3 exceptions into a single local exception. This has a drawback of squashing all exception classes into one. But if we ever want to properly try to handle one we can let specific ones propagate so they can be handled explicitly (this would happen in `pivot_exceptions()`).

## Installation

### Requirements
- Python 3.10+
- AWS credentials configured (see [AWS Credentials Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html))

### Install from GitHub

**Using uv (recommended):**
```bash
uv add git+https://github.com/crodenas/aws_v2.git
```

**Using pip:**
```bash
pip install git+https://github.com/crodenas/aws_v2.git
```

**Install a specific version/branch:**
```bash
uv add git+https://github.com/crodenas/aws_v2.git@v0.1.0
# or
pip install git+https://github.com/crodenas/aws_v2.git@main
```

### Install from source (for development)

```bash
git clone https://github.com/crodenas/aws_v2.git
cd aws_v2
uv install
# or for editable install with dev dependencies
uv pip install -e ".[dev]"
```

## Usage

Note: Because this package creates default boto3 service clients using the default boto3 session, you need to have `AWS_REGION` set somewhere. The ECS containers have AWS_REGION set by AWS. If it's not already set just set it in your environment.
See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

### Available Services

The library provides wrappers for the following AWS services:

- CloudFormation (`aws_v2.cloudformation`)
- CloudWatch (`aws_v2.cloudwatch`)
- DynamoDB (`aws_v2.dynamodb`)
- EC2 (`aws_v2.ec2`)
- IAM (`aws_v2.iam`)
- Identity Store (`aws_v2.identitystore`)
- CloudWatch Logs (`aws_v2.logs`)
- Organizations (`aws_v2.organizations`)
- S3 (`aws_v2.s3`)
- Service Catalog (`aws_v2.servicecatalog`)
- SES (`aws_v2.ses`)
- SQS (`aws_v2.sqs`)
- SSM (`aws_v2.ssm`)
- SSO Admin (`aws_v2.sso_admin`)
- STS (`aws_v2.sts`)

### Role Chaining Examples

#### New session in same region as default session
```python
>>> from aws_v2 import sts
>>> sts.session.region_name
'us-east-2'
>>> new_session = sts.assume_role(role_arn="arn:aws:iam::89xxxxxxxx96:role/Assumable_Role_1")
>>> new_session.region_name
'us-east-2'
```

#### Specifying region of new session
```python
>>> new_session = sts.assume_role(role_arn="arn:aws:iam::89xxxxxxxx96:role/Assumable_Role_1", region_name="us-west-1")
>>> new_session.region_name
'us-west-1'
```

**Note**: You could directly use the assumed role session to create service clients. But doing so you will not have the exceptions transformed into something local.

### Service Usage Examples

#### Making API calls with default client and session
```python
>>> from aws_v2 import identitystore as ids
>>> ids.list_groups(identitystore_id="d-9axxxxxxf8")
[{'GroupId': '015b6550-4011-70c6-aeb9-ed3ea48d2ed4', 'DisplayName': 'Admin', 'IdentityStoreId': 'd-9axxxxxxf8'}, {'GroupId': '81bb3570-2071-7005-11bb-8b1e7c8f0d40', 'DisplayName': 'PowerUsers', 'IdentityStoreId': 'd-9axxxxxxf8'}]
```

#### Exception Handling
All boto3 exceptions are transformed into local `AwsError` exceptions:
```python
>>> from aws_v2.exceptions import AwsError
>>> try:
...     ids.list_groups(identitystore_id="d-9axxxxxxf8")
... except AwsError as error:
...     print(f"Encounter an AWS error: {error}")
...
Encounter an AWS error: An error occurred in aws_v2.identitystore.list_groups: An error occurred (ResourceNotFoundException) when calling the ListGroups operation: IdentityStore not present for IdentityStoreId: d-9axxxxxxf8
```

## Development

### Running Tests

The project uses Python's unittest framework for testing. To run all tests:

```bash
uv run python -m unittest discover tests
```

Tests are organized in the `tests` directory, separate from the main package code.

### Code Quality

The project uses the following tools for code quality:
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting

To format and lint the code:
```bash
uv run black aws_v2 tests
uv run isort aws_v2 tests
uv run flake8 aws_v2 tests
```
