from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = "Reset the database"
    tables = ["apps_invoice", "apps_event", "apps_product", "apps_payment_method"]

    def sqlite_delete_table(self, table: str):
        with connection.cursor() as cursor:
            self.stdout.write(f"Deleting {table}")
            cursor.execute(f"DELETE FROM {table}")
            cursor.execute(f"DELETE FROM SQLITE_SEQUENCE WHERE name = '{table}'")

    def handle_sqlite(self):
        for table in self.tables:
            self.sqlite_delete_table(table)

    def handle_postgres(self):
        with connection.cursor() as cursor:
            for table in self.tables:
                self.stdout.write(f"Truncating {table}")
                cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")

    def handle(self, *args, **options):
        if not settings.USE_PSQL:
            self.handle_sqlite()
        else:
            self.handle_postgres()
        self.stdout.write(self.style.SUCCESS('Database reset complete'))