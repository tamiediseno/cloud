from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.transaction import Transaction
from real_estate.property import Property
from real_estate.tenant import Tenant

class Command(BaseCommand):
    help = 'Load fake data into the Transaction model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(250):
            property = Property.objects.order_by('?').first()
            tenant = Tenant.objects.order_by('?').first()
            buyer_name = fake.name()
            buyer_email = fake.email()
            buyer_phone_number = fake.phone_number()
            is_buying = fake.boolean()
            is_renting = fake.boolean()
            transaction = Transaction.objects.create(property=property, tenant=tenant, buyer_name=buyer_name, buyer_email=buyer_email, buyer_phone_number=buyer_phone_number, is_buying=is_buying, is_renting=is_renting)
            transaction.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded fake data into the Transaction model'))
