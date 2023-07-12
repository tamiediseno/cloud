from django.contrib.auth.models import User
from django.db import models

from cloudcheck import settings


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)