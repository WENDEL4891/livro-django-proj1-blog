from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                        .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager() # o gerenciador default
    published = PublishedManager() # nosso gerenciador personalizado

    def get_absolute_url(self):        

        local_time_publish = timezone.localtime(self.publish)

        return reverse('blog:post_detail',
                       args=[local_time_publish.year,
                             local_time_publish.month,
                             local_time_publish.day,
                             self.slug])
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
