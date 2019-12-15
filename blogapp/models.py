from django.db import models
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from captcha.fields import CaptchaField
from django.urls import reverse

class Post(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover           = models.ImageField(upload_to='images/', null=True)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    published_date  = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    class Meta():
        ordering = ['-published_date']


class NewComment(MPTTModel):
    post = models.ForeignKey(
        'blogapp.Post',
        on_delete=models.CASCADE,
        related_name='new_comments'
        )
    commented_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    parent          = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.text

    class MPTTMeta:
        order_insertion_by = ['created_date']

