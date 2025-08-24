"module"

from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions

client = session.client("servicecatalog")


@pivot_exceptions
def get_provisioned_product_outputs(
    provisioned_product_id: str = None,
    provisioned_product_name: str = None,
    servicecatalog_client: boto3.client = client,
) -> List:
    "function"
    results = []

    next_token: str = None
    while True:
        params = {
            "ProvisionedProductName": provisioned_product_name,
            "ProvisionedProductId": provisioned_product_id,
        }
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.scan_provisioned_products(**params)
        results.extend(response["ProvisionedProducts"])
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results


@pivot_exceptions
def scan_provisioned_products(
    servicecatalog_client: boto3.client = client,
) -> List:
    "function"
    results = []

    paginator = servicecatalog_client.get_paginator("scan_provisioned_products")
    for page in paginator.paginate():
        results.extend(page["ProvisionedProducts"])

    return results


@pivot_exceptions
def search_products(
    servicecatalog_client: boto3.client = client,
) -> List:
    "function"
    results = []

    next_token: str = None
    while True:
        params = {}
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.search_products(**params)
        results.extend(response["ProductViewSummaries"])
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results


@pivot_exceptions
def search_provisioned_products(
    servicecatalog_client: boto3.client = client,
) -> List:
    "function"
    results = []

    next_token: str = None
    while True:
        params = {}
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.search_provisioned_products(**params)
        results.extend(response["ProvisionedProducts"])
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results
