from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_browser = models.CharField(max_length=254, blank=True, null=True)
    user_device = models.CharField(max_length=254, blank=True, null=True)
    user_os = models.CharField(max_length=254, blank=True, null=True)
    def __str__(self):
        return self.email
