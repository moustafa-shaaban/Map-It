from django.core.management.base import BaseCommand
from django.db import transaction

from applications.places.models import Category, Place, Tag
from applications.places.factories import PlaceFactory, CategoryFactory, TagFactory

class Command(BaseCommand):
    help = 'Populate the database with realistic test data using Faker and Factory Boy'

    def add_arguments(self, parser):
        parser.add_argument(
            '--places',
            type=int,
            default=50,
            help='Number of places to create (default: 50)'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create (default: 10)'
        )
        parser.add_argument(
            '--tags',
            type=int,
            default=15,
            help='Number of tags to create (default: 15)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        places_count = options['places']
        categories_count = options['categories']
        tags_count = options['tags']
        clear = options['clear']

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Place.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared!'))

        self.stdout.write('Creating categories...')
        categories = CategoryFactory.create_batch(categories_count)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        self.stdout.write('Creating tags...')
        tags = TagFactory.create_batch(tags_count)
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags'))

        self.stdout.write(f'Creating {places_count} places...')
        places = []
        for i in range(places_count):
            if i % 10 == 0:
                self.stdout.write(f'  Progress: {i}/{places_count}')
            place = PlaceFactory()
            places.append(place)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(places)} places!'))
        
        # Display some statistics
        self.stdout.write('\n--- Database Statistics ---')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Tags: {Tag.objects.count()}')
        self.stdout.write(f'Places: {Place.objects.count()}')
