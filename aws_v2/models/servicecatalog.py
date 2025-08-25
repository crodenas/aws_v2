"""
Data models for AWS Service Catalog.
Contains dataclasses for provisioned products and related resources.
"""

from dataclasses import dataclass


@dataclass
class ProvisionedProductOutput:
    """
    Represents the output of a provisioned product.

    Attributes:
        id (str): The ID of the provisioned product.
        name (str): The name of the provisioned product.
        status (str): The status of the provisioned product.
        type (str): The type of the provisioned product.
        created_time (str): The creation time of the provisioned product.
    """

    id: str
    name: str
    status: str
    type: str
    created_time: str


@dataclass
class ScannedProvisionedProduct:
    """
    Represents a scanned provisioned product.

    Attributes:
        id (str): The ID of the provisioned product.
        name (str): The name of the provisioned product.
        status (str): The status of the provisioned product.
        type (str): The type of the provisioned product.
        created_time (str): The creation time of the provisioned product.
    """

    id: str
    name: str
    status: str
    type: str
    created_time: str


@dataclass
class ProductSummary:
    """
    Represents a summary of a product.

    Attributes:
        id (str): The ID of the product.
        name (str): The name of the product.
        owner (str): The owner of the product.
        product_type (str): The type of the product.
        short_description (str): A short description of the product.
    """

    id: str
    name: str
    owner: str
    product_type: str
    short_description: str


@dataclass
class SearchedProvisionedProduct:
    """
    Represents a searched provisioned product.

    Attributes:
        id (str): The ID of the provisioned product.
        name (str): The name of the provisioned product.
        status (str): The status of the provisioned product.
        type (str): The type of the provisioned product.
        created_time (str): The creation time of the provisioned product.
    """

    id: str
    name: str
    status: str
    type: str
    created_time: str
