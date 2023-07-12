from django.db import models
from real_estate.property import Property

class RentalProperty(models.Model):
 property = models.ForeignKey(Property, on_delete=models.CASCADE)
 bills_included_water_electricity = models.BooleanField(default=False)