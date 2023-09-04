from django.db import models
from user.models import UserModel

class TweetModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=256, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)