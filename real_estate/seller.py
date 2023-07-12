from django.db import models
from real_estate.property import Property


class Seller(models.Model):
 name = models.CharField(max_length=100)
 email = models.EmailField()
 phone_number = models.CharField(max_length=60)
 properties = models.ManyToManyField(Property)

 def __str__(self):
        return self.name
    
class Meta:
        verbose_name_plural = 'Seller'