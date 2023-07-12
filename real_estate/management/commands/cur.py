from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.currency import Currency


class Command(BaseCommand):
    help = 'Generates fake data for Currency'

    def handle(self, *args, **options):
        fake = Faker()

        for i in range(1000):
            currency = Currency.objects.create(
                name=fake.currency_name(),
                symbol=fake.currency_symbol(),
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created {currency}'))
