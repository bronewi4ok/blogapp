from django.db import models
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from captcha.fields import CaptchaField
from django.urls import reverse
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils.text import slugify

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_date__lte=timezone.now())

    def search(self, search_q):
        if search_q:
            post_range = self.published().filter(
                Q(title__icontains=search_q) |
                Q(text__icontains=search_q) 
            ).distinct()
        else:
            post_range = self.published()
        return post_range

    def author(self, q_author, current_user):
        if q_author == 'other':
            filter_author = self.published().exclude(author=current_user)
        elif q_author == 'my':
            filter_author = self.published().filter(author=current_user)
        else:
            filter_author = self.published().filter()
        return filter_author
    
    def date_range(self, q_date, filter_author):
        if q_date:
            data_range = timezone.now() - timedelta(days=int(q_date))
            post_range = filter_author.filter(published_date__gte=data_range)
        else:
            post_range = filter_author
        return post_range


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(published_date__lte=timezone.now())


class Post(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover           = models.ImageField(upload_to='images/%Y/%m/%d/', null=True)
    title           = models.CharField(max_length=200)
    text            = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    published_date  = models.DateTimeField(blank=True, null=True)
    slug_title      = models.SlugField(max_length=200, default='abc', blank=True, null=True)
    slug_date       = models.SlugField(default='abc', blank=True, null=True)
    slug_category   = models.SlugField(null=True, blank=True)
    category        = TreeForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)

    objects = PostQuerySet.as_manager()
    publishing = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title) or ''

    def get_absolute_url(self):
        return reverse('blogapp:post_detail', kwargs={'slug_title':self.slug_title, 'slug_date':self.slug_date })

    class Meta():
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
            self.slug_title = slugify(self.title)
            self.slug_date = slugify(self.created_date)
            # self.slug_category = slugify(self.category)
            super(Post, self).save(*args, **kwargs)



class Category(MPTTModel):
  name = models.CharField(max_length=50, unique=True)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
  slug = models.SlugField(blank=True)
  class MPTTMeta:
    order_insertion_by = ['name']

  class Meta:
    unique_together = (('parent', 'slug',))
    verbose_name_plural = 'categories'

  def get_slug_list(self):
    try:
      ancestors = self.get_ancestors(include_self=True)
    except:
      ancestors = []
    else:
      ancestors = [ i.slug for i in ancestors]
    slugs = []
    for i in range(len(ancestors)):
      slugs.append('/'.join(ancestors[:i+1]))
    return slugs

  def __str__(self):
    return str(self.name) or ''



class NewComment(MPTTModel):
    post = models.ForeignKey(
        'blogapp.Post',
        on_delete=models.CASCADE,
        related_name='new_comments'
        )

    commented_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text            = models.TextField(max_length=900)
    created_date    = models.DateTimeField(default=timezone.now)
    parent          = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
    
    def __str__(self):
        return str(self.commented_by) or ''

    class MPTTMeta:
        order_insertion_by = ['-created_date']



class Slider(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='image/slider/%id', blank=True)
    title = models.CharField(max_length=200, blank=True, default="Title")
    caption = models.CharField(max_length=50, blank=True, default="Caption")
    position = models.PositiveIntegerField(unique=True, default=0)
    show = models.BooleanField(default = True)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['position']
