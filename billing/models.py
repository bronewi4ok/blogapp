from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver


class BillingProfile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email           = models.EmailField(max_length=254)
    timestamp       = models.DateTimeField( auto_now_add=True )
    updated         = models.DateTimeField(auto_now=True)
    active          = models.BooleanField(default=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created_reciver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance)
