import csv
import random
from random import choice

from django.core.management.base import BaseCommand
from api.models import Location, Car


class Command(BaseCommand):
    help = 'Loads initial data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            locations = [
                Location(
                    zip_code=row[0],
                    latitude=float(row[1]),
                    longitude=float(row[2]),
                    city=row[3],
                    state=row[4],

                )
                for row in reader
            ]

            Location.objects.bulk_create(locations)

        self.stdout.write(self.style.SUCCESS('Locations loaded successfully!'))

        for _ in range(20):
            random_location = choice(Location.objects.all())
            Car.objects.create(
                unique_number=f'{random.randrange(1000, 9999)}A',
                current_location=random_location,
                carrying_capacity=random.randrange(0, 1000)
            )
        self.stdout.write(self.style.SUCCESS('Cars were created successfully!'))
