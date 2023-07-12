from django.db import models
from cloudcheck import settings
from real_estate.property import Property
from django.contrib.auth.models import User





class Tenant(models.Model):
 email = models.EmailField()
 phone_number = models.CharField(max_length=60)
 properties = models.ManyToManyField(Property, through='Transaction')
 user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 
 def __str__(self):
    return self.name
    
class Meta:
        verbose_name_plural = 'Tenant'

