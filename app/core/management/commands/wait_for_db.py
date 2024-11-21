import time
from typing import Any
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until the database is available."""

    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        self.stdout.write('Waiting for database...')
        db_up = False

        while not db_up:
            try:
                connections['default'].ensure_connection()
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
