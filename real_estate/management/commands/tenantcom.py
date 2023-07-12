from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.tenant import Tenant
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load fake data into the Tenant model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(10):
            name = fake.name()
            email = fake.email()
            phone_number = fake.phone_number()
            user = User.objects.create_user(username=email, email=email)
            tenant = Tenant.objects.create(name=name, email=email, phone_number=phone_number, user_id=user.id)
            tenant.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded fake data into the Tenant model'))
