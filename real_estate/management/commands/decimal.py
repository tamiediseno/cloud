from decimal import Decimal
from real_estate.property import Property
from django.core.management.base import BaseCommand


class Command(BaseCommand):
 def handle(self, *args, **kwargs):
    properties = Property.objects.all()
    for property in properties:
    # check the value of the price field
     price = property.price
    if not isinstance(price, Decimal):
        # handle invalid data
        print(f'Invalid price data for Property with id {property.id}: {price}')
