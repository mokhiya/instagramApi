from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)


class VerificationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verification')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.code}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Codes'
        unique_together = (('user', 'code'),)


class FollowModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} following to {self.to_user.email}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
        unique_together = (('user', 'to_user'),)

