from django.contrib import admin

from posts.models import PostModel, CommentModel, CommentLikeModel, PostLikeModel, HistoryModel

admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(CommentLikeModel)
admin.site.register(PostLikeModel)
admin.site.register(HistoryModel)

