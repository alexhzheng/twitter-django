from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    tweet_likes = models.ManyToManyField(User, related_name='likes')
    hashtag = models.ManyToManyField("Hashtag", related_name="tweets")
    class Meta: 
        ordering = ['-timestamp']

class Hashtag(models.Model):
    tag = models.CharField(max_length=100)

class Person(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    followerNum = models.PositiveIntegerField(default=0)
    followingNum = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField(User, related_name='followingNum')
    followers = models.ManyToManyField(User, related_name='followerNum')


