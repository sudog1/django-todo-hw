from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    profile_picture = models.ImageField(null=True, blank=True)
