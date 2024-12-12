from unittest.mock import patch, MagicMock
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class WaitForDBCommandTest(TestCase):
    """Test the wait_for_db management command."""

    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db_ready(self, mock_getitem):
        """Test wait_for_db when the database is available."""
        # simulate a successful connection to the database
        mock_connection = MagicMock()
        mock_connection.ensure_connection.return_value = True
        mock_getitem.return_value = mock_connection

        call_command('wait_for_db')

        # Ensure that the connection was attempted
        mock_connection.ensure_connection.assert_called_once()

    @patch('time.sleep', return_value=None)  # Mock sleep for faster testsu
    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db_delay(self, mock_getitem, mock_sleep):
        """Test wait_for_db avec des erreurs initiales."""
        # simulate 5 failed connections before a successful connection
        mock_connection = MagicMock()
        mock_connection.ensure_connection.side_effect = [OperationalError] * 5 + [True]
        mock_getitem.return_value = mock_connection

        call_command('wait_for_db')
        self.assertEqual(mock_connection.ensure_connection.call_count, 6)
