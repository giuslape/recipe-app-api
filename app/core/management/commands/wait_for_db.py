"""
Django commands to wait fot the database to be available
"""
import os

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database to be available"""

    def handle(self, *args, **options):
        """Entrypoint for the management command"""
        self.stdout.write('Waiting for database...')
        db_conn = False
        while db_conn is False:
            try:
                self.check(databases=['default'])
                db_conn = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(self.style.WARNING('Database unavailable, \
                waiting 1 second...'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
