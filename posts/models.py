from django.db import models

from users.models import CustomUser


class PostModel(models.Model):
    parent = models.ForeignKey('self', related_name='children',
                               on_delete=models.CASCADE,
                               blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

# class LikeModel(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
#     post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
#     created_at = models.DateTimeField(auto_now_add=True)

