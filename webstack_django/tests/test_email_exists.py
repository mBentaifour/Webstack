import unittest
from unittest.mock import patch, MagicMock
from auth_.utils.db_get_data import email_exists  # Correct import path

class TestEmailExists(unittest.TestCase):
    @patch("auth_.utils.db_get_data.engine.connect")
    def test_email_exists_true(self, mock_connect):
        # Mock the connection and query execution
        mock_connection = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_connection
        mock_result = MagicMock()
        mock_result.scalar.return_value = True  # Simulate email exists
        mock_connection.execute.return_value = mock_result

        result = email_exists("test@gmail.com")
        self.assertTrue(result)

    @patch("auth_.utils.db_get_data.engine.connect")
    def test_email_exists_false(self, mock_connect):
        # Mock the connection and query execution
        mock_connection = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_connection
        mock_result = MagicMock()
        mock_result.scalar.return_value = False  # Simulate email does not exist
        mock_connection.execute.return_value = mock_result

        result = email_exists("notfound@gmail.com")
        self.assertFalse(result)

    @patch("auth_.utils.db_get_data.engine.connect")
    def test_email_exists_exception(self, mock_connect):
        mock_connect.side_effect = Exception("Database error")

        result = email_exists("error@gmail.com")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
