# boto3 interface library

## Purpose
This library is desinged as an abstraction on top of boto3 to allow easy proper role chaining.  By using the service modules implemented here, it also transforms all boto3 exceptions into a single local exception.  This has a drawback of squashing all exception classes into one.  But if we ever want to properly try to handle one we can let specific ones propagate so they can be handled explicitly (this would happen in `pivot_exceptions()`)

### Usage

Note: Because this package creates default boto3 service clients using the default boto3 session, you need to have `AWS_REGION` set somewhere.  The ECS containers have AWS_REGION set by AWS.  If it's not already set just set it in your environment.
See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#



#### New session is in same region as default session
```sh
>>> from aws_v2 import sts
>>> sts.session.region_name
'us-east-2'
>>> new_session = sts.assume_role(role_arn="arn:aws:iam::89xxxxxxxx96:role/Assumable_Role_1")
>>> new_session.region_name
'us-east-2'
>>>
```

#### Specifying region of new session
```sh
>>> new_session = sts.assume_role(role_arn="arn:aws:iam::89xxxxxxxx96:role/Assumable_Role_1", region_name="us-west-1")
>>> new_session.region_name
'us-west-1'
>>>
```

**Note**: You could directly use the assumed role session to create service clients.  But doing so you will not have the excptions transformed into something local.

#### All boto3 exceptions are pivoting into local exceptions
```sh
>>> from aws_v2.exceptions import AwsError
>>> try:
...     ids.list_groups(identitystore_id="d-9axxxxxxf8")
... except AwsError as error:
...     print(f"Encounter an AWS error: {error}")
...
Encounter an AWS error: An error occurred in aws_v2.identitystore.list_groups: An error occurred (ResourceNotFoundException) when calling the ListGroups operation: IdentityStore not present for IdentityStoreId: d-9axxxxxxf8
>>>
```

#### Making API call with default client and session
```sh
>>> from aws_v2 import identitystore as ids
>>> ids.list_groups(identitystore_id="d-9axxxxxxf8")
[{'GroupId': '015b6550-4011-70c6-aeb9-ed3ea48d2ed4', 'DisplayName': 'Admin', 'IdentityStoreId': 'd-9axxxxxxf8'}, {'GroupId': '81bb3570-2071-7005-11bb-8b1e7c8f0d40', 'DisplayName': 'PowerUsers', 'IdentityStoreId': 'd-9axxxxxxf8'}]
>>>
```
