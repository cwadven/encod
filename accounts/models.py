from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    nickname = models.CharField(max_length=13, unique=True, blank=False)

    def __str__(self):
        return '%s' % (self.username)