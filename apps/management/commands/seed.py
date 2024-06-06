import pathlib
import pandas as pd
from django.core.management.base import BaseCommand
from apps.models import Product, Event

class Command(BaseCommand):
    help = 'Seed the database with data from CSV files'

    def handle(self, *args, **kwargs):
        self.seed_products()
        self.seed_events()

    def seed_products(self):
        productcsv = pathlib.Path(__file__).parent.absolute().joinpath("product.csv")
        df = pd.read_csv(productcsv)
        for _, row in df.iterrows():
            Product.objects.create(
                product_name=row['product_name'],
                description=row['description'],
                price=row['price']
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Product data'))

    def seed_events(self):
        eventcsv = pathlib.Path(__file__).parent.absolute().joinpath("events.csv")
        df = pd.read_csv(eventcsv)
        for _, row in df.iterrows():
            Event.objects.create(
                event_name=row['event_name'],
                description=row['description']
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Event data'))
