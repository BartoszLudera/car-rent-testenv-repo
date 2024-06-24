from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    visible_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phonenumber = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    nip = models.CharField(max_length=10, blank=True, null=True)
    regulamin = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)

    def __str__(self):
        return self.username
