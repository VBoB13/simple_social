from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text="Limit: 100 characters.")
    content = models.TextField(max_length=1024, help_text="Limit: 1024 characters.")
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('posts:index')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=512, help_text="Limit: 512 characters.")
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):
        return "{}".format(self.user)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={
            "pk": self.post.pk
        })
    
