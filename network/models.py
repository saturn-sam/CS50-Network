from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='folowers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    class Meta:

        unique_together = ['following', 'follower']

    def __str__(self):
        return f"{self.follower} is following {self.following}"

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    @property
    def num_likes(self):
        return self.liked.all().count()