"""Unit tests for SSM Parameter Store functions."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from aws_v2.models.ssm import Parameter
from aws_v2.ssm import (
    delete_parameter,
    get_parameter,
    get_parameters_by_path,
    put_parameter,
)


class TestSSM(unittest.TestCase):
    """Test cases for SSM Parameter Store functions."""

    def setUp(self):
        """Set up common test data for SSM tests."""
        self.mock_ssm = MagicMock()
        self.test_parameter = Parameter(
            name="/test/parameter",
            value="test-value",
            last_modified_date=datetime(2025, 12, 17, 12, 0, 0),
        )

    @patch("aws_v2.ssm.client")
    def test_delete_parameter(self, mock_client):
        """Test delete_parameter removes a parameter."""
        delete_parameter("/test/parameter", mock_client)
        mock_client.delete_parameter.assert_called_once_with(
            Name="/test/parameter"
        )

    def test_delete_parameter_with_custom_client(self):
        """Test delete_parameter with custom SSM client."""
        delete_parameter("/custom/parameter", self.mock_ssm)
        self.mock_ssm.delete_parameter.assert_called_once_with(
            Name="/custom/parameter"
        )

    @patch("aws_v2.ssm.client")
    def test_get_parameter(self, mock_client):
        """Test get_parameter retrieves parameter data."""
        mock_response = {
            "Parameter": {
                "Name": "/test/parameter",
                "Value": "test-value",
                "LastModifiedDate": datetime(2025, 12, 17, 12, 0, 0),
            }
        }
        mock_client.get_parameter.return_value = mock_response

        result = get_parameter(
            "/test/parameter", decrypt=True, ssm_client=mock_client
        )

        self.assertEqual(result.name, "/test/parameter")
        self.assertEqual(result.value, "test-value")
        self.assertEqual(
            result.last_modified_date, datetime(2025, 12, 17, 12, 0, 0)
        )
        mock_client.get_parameter.assert_called_once_with(
            Name="/test/parameter", WithDecryption=True
        )

    def test_get_parameter_no_decrypt(self):
        """Test get_parameter without decryption."""
        mock_response = {
            "Parameter": {
                "Name": "/test/encrypted",
                "Value": "encrypted-value",
                "LastModifiedDate": datetime(2025, 12, 17, 12, 0, 0),
            }
        }
        self.mock_ssm.get_parameter.return_value = mock_response

        result = get_parameter(
            "/test/encrypted", decrypt=False, ssm_client=self.mock_ssm
        )

        self.assertEqual(result.name, "/test/encrypted")
        self.assertEqual(result.value, "encrypted-value")
        self.mock_ssm.get_parameter.assert_called_once_with(
            Name="/test/encrypted", WithDecryption=False
        )

    def test_get_parameters_by_path(self):
        """Test get_parameters_by_path retrieves multiple parameters."""
        mock_paginator = MagicMock()
        self.mock_ssm.get_paginator.return_value = mock_paginator

        # Set up mock paginator to return parameters across multiple pages
        mock_paginator.paginate.return_value = [
            {
                "Parameters": [
                    {
                        "Name": "/app/config/db_host",
                        "Value": "localhost",
                        "LastModifiedDate": datetime(2025, 12, 1, 10, 0, 0),
                    },
                    {
                        "Name": "/app/config/db_port",
                        "Value": "5432",
                        "LastModifiedDate": datetime(2025, 12, 2, 11, 0, 0),
                    },
                ]
            },
            {
                "Parameters": [
                    {
                        "Name": "/app/config/db_name",
                        "Value": "mydb",
                        "LastModifiedDate": datetime(2025, 12, 3, 12, 0, 0),
                    }
                ]
            },
        ]

        result = get_parameters_by_path(
            "/app/config", decrypt=True, ssm_client=self.mock_ssm
        )

        # Verify results
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "/app/config/db_host")
        self.assertEqual(result[0].value, "localhost")
        self.assertEqual(
            result[0].last_modified_date, datetime(2025, 12, 1, 10, 0, 0)
        )
        self.assertEqual(result[1].name, "/app/config/db_port")
        self.assertEqual(result[1].value, "5432")
        self.assertEqual(result[2].name, "/app/config/db_name")
        self.assertEqual(result[2].value, "mydb")

        # Verify paginator was used correctly
        self.mock_ssm.get_paginator.assert_called_once_with(
            "get_parameters_by_path"
        )
        mock_paginator.paginate.assert_called_once_with(
            Path="/app/config", WithDecryption=True
        )

    def test_get_parameters_by_path_no_decrypt(self):
        """Test get_parameters_by_path without decryption."""
        mock_paginator = MagicMock()
        self.mock_ssm.get_paginator.return_value = mock_paginator

        mock_paginator.paginate.return_value = [
            {
                "Parameters": [
                    {
                        "Name": "/app/secret",
                        "Value": "encrypted",
                        "LastModifiedDate": datetime(2025, 12, 17, 12, 0, 0),
                    }
                ]
            }
        ]

        result = get_parameters_by_path(
            "/app", decrypt=False, ssm_client=self.mock_ssm
        )

        self.assertEqual(len(result), 1)
        mock_paginator.paginate.assert_called_once_with(
            Path="/app", WithDecryption=False
        )

    @patch("aws_v2.ssm.client")
    def test_put_parameter(self, mock_client):
        """Test put_parameter stores a parameter."""
        put_parameter(
            self.test_parameter,
            overwrite=True,
            param_type="SecureString",
            ssm_client=mock_client,
        )

        mock_client.put_parameter.assert_called_once_with(
            Name="/test/parameter",
            Value="test-value",
            Overwrite=True,
            Type="SecureString",
        )

    def test_put_parameter_string_type(self):
        """Test put_parameter with String type."""
        parameter = Parameter(name="/test/plain", value="plain-text")

        put_parameter(
            parameter,
            overwrite=False,
            param_type="String",
            ssm_client=self.mock_ssm,
        )

        self.mock_ssm.put_parameter.assert_called_once_with(
            Name="/test/plain",
            Value="plain-text",
            Overwrite=False,
            Type="String",
        )

    def test_put_parameter_default_values(self):
        """Test put_parameter with default parameter values."""
        parameter = Parameter(name="/test/default", value="default-value")

        put_parameter(parameter, ssm_client=self.mock_ssm)

        self.mock_ssm.put_parameter.assert_called_once_with(
            Name="/test/default",
            Value="default-value",
            Overwrite=True,
            Type="SecureString",
        )


if __name__ == "__main__":
    unittest.main()
