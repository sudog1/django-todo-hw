from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    profile_image = models.ImageField(null=True, blank=True)
