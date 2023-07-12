import os
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from real_estate.property import Property
from real_estate.currency import Currency
from real_estate.models import AccessKey
from djmoney.models.fields import Money, MoneyField
from decimal import Decimal
from PIL import Image
import random

class Command(BaseCommand):
    help = 'Generates fake data for Property'

    def handle(self, *args, **options):
        fake = Faker()

        # Create a new Currency instance
        currency = Currency.objects.create(
            name='US Dollar',
            symbol='$',
        )

        # Create a new AccessKey instance
        access_key = AccessKey.objects.create(
            username=fake.user_name(),
                email=fake.email(),
                access_key=fake.random_int(min=2, max=6),
                phone_number=fake.random_int(min=1, max=12),
                is_staff=False,
                is_superuser=False,
            
        )

        # Set the path to the directory where the fake images will be saved
        # Set the path to the directory where the fake images will be saved
        image_dir = 'C:\\Users\\user\\Desktop\\cloud_archers\\media\\media'


        for i in range(20):
            # Generate a fake image using Pillow
            width, height = 200, 200
            image = Image.new('RGB', (width, height))
            pixels = image.load()
            for x in range(width):
                for y in range(height):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    pixels[x, y] = (r, g, b)

            # Save the fake image to the specified directory
            image_path = os.path.join(image_dir, f'fake_image_{i}.png')
            image.save(image_path)

            # Open the fake image file
            with open(image_path, 'rb') as f:
                image_file = File(f)

                # Create a new Property instance with the fake image
                property = Property.objects.create(
                    name=access_key,
                    description=fake.text(),
                    price=Decimal(fake.random_int(min=100000, max=300000)),
                    currency=currency,
                    image=image_file,
                    is_for_sale=True,
                    is_for_rent=False,
                    is_stand_for_sale=False,
                    room_size=fake.random_int(min=10, max=50),
                    number_of_rooms=fake.random_int(min=1, max=5),
                    location=fake.address(),
                    city=fake.city(),
                    bills_included_water_electricity=True,
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created {property}'))
