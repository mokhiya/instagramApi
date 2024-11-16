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


class CommentModel(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    image = models.ImageField(upload_to='comments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} - {self.text[:20]}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class PostLikeModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'PostLike'
        verbose_name_plural = 'PostLikes'
        unique_together = (('user', 'post'),)


class CommentLikeModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'CommentLike'
        verbose_name_plural = 'CommentLikes'
        unique_together = (('user', 'comment'),)

