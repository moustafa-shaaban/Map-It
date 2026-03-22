from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_save
from factory.django import mute_signals
from applications.users.factories import UserFactory

class Command(BaseCommand):
    help = 'Script used for populating the database with users and profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', 
            type=int, 
            default=10, 
            help='number of users to generate'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(self.style.SUCCESS(f'Generating {count} users...'))

        
        with transaction.atomic():
            with mute_signals(post_save):
                users = UserFactory.create_batch(count)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {len(users)} users with their profiles.')
        )