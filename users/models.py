from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)


class VerificationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
