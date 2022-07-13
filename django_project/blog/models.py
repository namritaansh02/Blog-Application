from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    votes = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})


class Activity(models.Model):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices = ACTIVITY_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    content = models.TextField()
    votes = models.IntegerField(default = 0)
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def get_time(self):
        dt = self.date_posted - self.post.date_posted
        if dt.seconds//60==0:
            return str(dt.seconds) + ' second' + 's'*(dt.seconds>1) + ' ago'
        if dt.seconds//3600==0:
            return str(dt.seconds//60) + ' minute' + 's'*(dt.seconds//60>1) + ' ago'
        if dt.days==0:
            return str(dt.seconds//3600) + ' hour' + 's'*(dt.seconds//3600>1) + ' ago'
        if dt.days!=0:
            return str(dt.days) + ' day' + 's'*(dt.days>1) + ' ago'

    def get_absolute_url(self):
        print(self.post.pk)
        return reverse('post-detail', kwargs={'pk':self.post.pk})
