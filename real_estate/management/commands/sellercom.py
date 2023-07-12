from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.seller import Seller

class Command(BaseCommand):
    help = 'Load fake data into the Seller model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(100):
            name = fake.name()
            email = fake.email()
            phone_number = fake.phone_number()
            seller = Seller.objects.create(name=name, email=email, phone_number=phone_number)
            seller.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded fake data into the Seller model'))
