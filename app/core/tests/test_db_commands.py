from unittest.mock import patch, MagicMock
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


@patch('core.management.commands.wait_for_db.Command.check')
class DBCommandTests(TestCase):
    def test_wait_for_db_ready(self, patched_check: MagicMock) -> None:
        """ Test that the command finishes immediately if the database is ready."""
        patched_check.return_value = True  # Simulate that the database is ready
        call_command('wait_for_db')
        patched_check.assert_called_once()  # Verify that it was called only once

    @patch('time.sleep')  # Mock `time.sleep` to avoid actual delays
    def test_wait_for_db_delay(self, patched_sleep: MagicMock, patched_check: MagicMock) -> None:
        """ Test the command retries multiple times before the database is ready. """
        # Simulate several failures before the database becomes available
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        call_command('wait_for_db')

        # Verify that `check` was called 6 times (5 failures + 1 success)
        self.assertEqual(patched_check.call_count, 6)
