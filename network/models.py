from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name="followers")
    

class Post(models.Model):
    posting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts')