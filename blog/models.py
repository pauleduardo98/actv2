from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    authorblog = models.ForeignKey('auth.User')
    titleblog = models.CharField(max_length=200)
    textblog = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.titleblog

        