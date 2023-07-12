from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.models import AccessKey



class Command(BaseCommand):
    help = 'Generates fake data for Access Key'

    def handle(self, *args, **options):
        fake = Faker()

        
        for i in range(20):
            access = AccessKey.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                access_key=fake.random_int(min=2, max=6),
                phone_number=fake.random_int(min=1, max=12),
                is_staff=False,
                is_superuser=False,
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created {access}'))
