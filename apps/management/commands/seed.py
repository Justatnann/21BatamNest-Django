import pathlib
from django.core.management.base import BaseCommand
import csv
from apps.models import Product, Event

class Command(BaseCommand):
    help = 'Seed the database with data from CSV files'

    def handle(self, *args, **kwargs):
        self.seed_products()
        self.seed_events()

    def seed_products(self):
        productcsv = pathlib.Path(__file__).parent.absolute().joinpath("product.csv")
        with open(productcsv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Product.objects.create(
                    product_name=row['product_name'],
                    description=row['description'],
                    price=row['price']
                )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Product data'))

    def seed_events(self):
        eventcsv = pathlib.Path(__file__).parent.absolute().joinpath("events.csv")
        with open(eventcsv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Event.objects.create(
                    event_name=row['event_name'],
                    description=row['description']
                )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Event data'))