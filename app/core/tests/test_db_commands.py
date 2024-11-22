from unittest.mock import patch, MagicMock
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('django.db.connections')
class DBCommandTests(SimpleTestCase):
    # def test_wait_for_db_ready(self, patched_connections: MagicMock) -> None:
    #     """Test that the command finishes immediately if the database is ready."""
    #     # Mock the database connection to behave as if the database is ready
    #     patched_connections['default'].ensure_connection.return_value = None
    #
    #     # Call the command
    #     call_command('wait_for_db')
    #
    #     # Assert ensure_connection was called exactly once
    #     patched_connections['default'].ensure_connection.assert_called_once()

    @patch('time.sleep')  # Mock `time.sleep` to avoid actual delays
    def test_wait_for_db_delay(self, patched_sleep: MagicMock, patched_connections: MagicMock) -> None:
        """Test the command retries multiple times before the database is ready."""
        # Simulate several failures before the database becomes available
        patched_connections['default'].ensure_connection.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [None]
        )

        # Call the command
        call_command('wait_for_db')

        # Verify that `ensure_connection` was called 6 times (5 failures + 1 success)
        self.assertEqual(patched_connections['default'].ensure_connection.call_count, 6)
