"""Unit tests for the servicecatalog module in aws_v2 package."""

import unittest
from unittest.mock import patch

from aws_v2.servicecatalog import (ProductSummary, ProvisionedProductOutput,
                                   ScannedProvisionedProduct,
                                   SearchedProvisionedProduct,
                                   get_provisioned_product_outputs,
                                   scan_provisioned_products, search_products,
                                   search_provisioned_products)


class TestServiceCatalog(unittest.TestCase):
    """Unit tests for the Service Catalog module."""

    def setUp(self):
        """Set up common test data for ServiceCatalog tests."""
        self.mock_response = {
            "ProvisionedProducts": [
                {
                    "Id": "prod-123",
                    "Name": "TestProduct",
                    "Status": "AVAILABLE",
                    "Type": "CLOUD_FORMATION_TEMPLATE",
                    "CreatedTime": "2025-08-24T12:00:00Z",
                }
            ]
        }

    @patch("aws_v2.servicecatalog.client")
    def test_get_provisioned_product_outputs(self, mock_client):
        """Test get_provisioned_product_outputs returns expected output."""
        mock_client.scan_provisioned_products.return_value = self.mock_response
        result = get_provisioned_product_outputs(provisioned_product_id="prod-123")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ProvisionedProductOutput)
        self.assertEqual(result[0].id, "prod-123")
        self.assertEqual(result[0].name, "TestProduct")
        self.assertEqual(result[0].status, "AVAILABLE")

    @patch("aws_v2.servicecatalog.client")
    def test_scan_provisioned_products(self, mock_client):
        """Test the scan_provisioned_products function."""
        # Mock response
        mock_response = {
            "ProvisionedProducts": [
                {
                    "Id": "prod-456",
                    "Name": "ScannedProduct",
                    "Status": "AVAILABLE",
                    "Type": "CLOUD_FORMATION_TEMPLATE",
                    "CreatedTime": "2025-08-24T12:00:00Z",
                }
            ]
        }
        mock_client.get_paginator.return_value.paginate.return_value = [mock_response]

        # Call the function
        result = scan_provisioned_products()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ScannedProvisionedProduct)
        self.assertEqual(result[0].id, "prod-456")
        self.assertEqual(result[0].name, "ScannedProduct")

    @patch("aws_v2.servicecatalog.client")
    def test_search_products(self, mock_client):
        """Test the search_products function."""
        # Mock response
        mock_response = {
            "ProductViewSummaries": [
                {
                    "ProductId": "prod-789",
                    "Name": "TestProduct",
                    "Owner": "TestOwner",
                    "Type": "CLOUD_FORMATION_TEMPLATE",
                    "ShortDescription": "A test product",
                }
            ]
        }
        mock_client.search_products.return_value = mock_response

        # Call the function
        result = search_products()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ProductSummary)
        self.assertEqual(result[0].id, "prod-789")
        self.assertEqual(result[0].name, "TestProduct")
        self.assertEqual(result[0].owner, "TestOwner")

    @patch("aws_v2.servicecatalog.client")
    def test_search_provisioned_products(self, mock_client):
        """Test the search_provisioned_products function."""
        # Mock response
        mock_response = {
            "ProvisionedProducts": [
                {
                    "Id": "prod-101",
                    "Name": "SearchedProduct",
                    "Status": "AVAILABLE",
                    "Type": "CLOUD_FORMATION_TEMPLATE",
                    "CreatedTime": "2025-08-24T12:00:00Z",
                }
            ]
        }
        mock_client.search_provisioned_products.return_value = mock_response

        # Call the function
        result = search_provisioned_products()

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], SearchedProvisionedProduct)
        self.assertEqual(result[0].id, "prod-101")
        self.assertEqual(result[0].name, "SearchedProduct")


if __name__ == "__main__":
    unittest.main()
