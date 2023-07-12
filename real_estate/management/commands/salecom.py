from django.core.management.base import BaseCommand
from faker import Faker
from real_estate.sale import Sale
from real_estate.transaction import Transaction

class Command(BaseCommand):
    help = 'Load fake data into the Sale model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(250):
            transaction = Transaction.objects.order_by('?').first()
            payment_method = fake.word()
            sale = Sale.objects.create(transaction=transaction, payment_method=payment_method)
            sale.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded fake data into the Sale model'))
