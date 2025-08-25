"""
This module provides functions to interact with AWS Service Catalog, including retrieving
and searching provisioned products and products.
"""

from typing import List

import boto3

from . import session
from .exceptions import pivot_exceptions
from .models.servicecatalog import (ProductSummary, ProvisionedProductOutput,
                                    ScannedProvisionedProduct,
                                    SearchedProvisionedProduct)

client = session.client("servicecatalog")


@pivot_exceptions
def get_provisioned_product_outputs(
    provisioned_product_id: str = None,
    provisioned_product_name: str = None,
    servicecatalog_client: boto3.client = None,
) -> List[ProvisionedProductOutput]:
    """
    Retrieves the outputs of provisioned products.

    Args:
        provisioned_product_id (str, optional): The ID of the provisioned product.
        provisioned_product_name (str, optional): The name of the provisioned product.
        servicecatalog_client (boto3.client, optional): A boto3 Service Catalog client.

    Returns:
        List[ProvisionedProductOutput]: A list of provisioned product outputs.
    """
    results = []

    if servicecatalog_client is None:
        servicecatalog_client = client

    next_token: str = None
    while True:
        params = {
            "ProvisionedProductName": provisioned_product_name,
            "ProvisionedProductId": provisioned_product_id,
        }
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.scan_provisioned_products(**params)
        for product in response["ProvisionedProducts"]:
            results.append(
                ProvisionedProductOutput(
                    id=product.get("Id"),
                    name=product.get("Name"),
                    status=product.get("Status"),
                    type=product.get("Type"),
                    created_time=product.get("CreatedTime"),
                )
            )
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results


@pivot_exceptions
def scan_provisioned_products(
    servicecatalog_client: boto3.client = None,
) -> List[ScannedProvisionedProduct]:
    """
    Scans all provisioned products.

    Args:
        servicecatalog_client (boto3.client, optional): A boto3 Service Catalog client.

    Returns:
        List[ScannedProvisionedProduct]: A list of scanned provisioned products.
    """
    results = []

    if servicecatalog_client is None:
        servicecatalog_client = client

    paginator = servicecatalog_client.get_paginator("scan_provisioned_products")
    for page in paginator.paginate():
        for product in page["ProvisionedProducts"]:
            results.append(
                ScannedProvisionedProduct(
                    id=product.get("Id"),
                    name=product.get("Name"),
                    status=product.get("Status"),
                    type=product.get("Type"),
                    created_time=product.get("CreatedTime"),
                )
            )

    return results


@pivot_exceptions
def search_products(
    servicecatalog_client: boto3.client = None,
) -> List[ProductSummary]:
    """
    Searches for products in the Service Catalog.

    Args:
        servicecatalog_client (boto3.client, optional): A boto3 Service Catalog client.

    Returns:
        List[ProductSummary]: A list of product summaries.
    """
    results = []

    if servicecatalog_client is None:
        servicecatalog_client = client

    next_token: str = None
    while True:
        params = {}
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.search_products(**params)
        for product in response["ProductViewSummaries"]:
            results.append(
                ProductSummary(
                    id=product.get("ProductId"),
                    name=product.get("Name"),
                    owner=product.get("Owner"),
                    product_type=product.get("Type"),
                    short_description=product.get("ShortDescription"),
                )
            )
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results


@pivot_exceptions
def search_provisioned_products(
    servicecatalog_client: boto3.client = None,
) -> List[SearchedProvisionedProduct]:
    """
    Searches for provisioned products in the Service Catalog.

    Args:
        servicecatalog_client (boto3.client, optional): A boto3 Service Catalog client.

    Returns:
        List[SearchedProvisionedProduct]: A list of searched provisioned products.
    """
    results = []

    if servicecatalog_client is None:
        servicecatalog_client = client

    next_token: str = None
    while True:
        params = {}
        if next_token:
            params["PageToken"] = next_token
        response = servicecatalog_client.search_provisioned_products(**params)
        for product in response["ProvisionedProducts"]:
            results.append(
                SearchedProvisionedProduct(
                    id=product.get("Id"),
                    name=product.get("Name"),
                    status=product.get("Status"),
                    type=product.get("Type"),
                    created_time=product.get("CreatedTime"),
                )
            )
        next_token = response.get("NextPageToken")
        if not next_token:
            break

    return results
