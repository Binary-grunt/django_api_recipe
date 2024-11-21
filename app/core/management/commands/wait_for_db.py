import time

from django.db import connections
from typing import Any
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        """ Main logic of the `wait_for_db` command. It waits until the database is ready. """
        self.stdout.write('Waiting for database...')  # Notify the user that the command is running
        db_up: bool = False

        while db_up is False:
            try:
                connections['default'].cursor()
                db_up = True  # Mark database as ready
            except (Psycopg2Error, OperationalError):
                # Notify the user that the database is unavailable
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)  # Wait before retrying

        # Notify the user that the database is available
        self.stdout.write(self.style.SUCCESS('Database available!'))
