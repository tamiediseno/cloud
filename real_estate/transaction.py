from django.db import models
from real_estate.property import Property
from real_estate.tenant import Tenant


class Transaction(models.Model):
 property = models.ForeignKey(Property, on_delete=models.CASCADE)
 tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
 buyer_name = models.CharField(max_length=100)
 buyer_email = models.EmailField()
 buyer_phone_number = models.CharField(max_length=60)
 is_buying = models.BooleanField(default=False)
 is_renting = models.BooleanField(default=False)
 time_of_transaction = models.DateTimeField(auto_now_add=True)

 def __str__(self):
        return self.buyer_name
    
class Meta:
        verbose_name_plural = 'Transaction'
