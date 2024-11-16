from rest_framework.routers import DefaultRouter
from django.urls import path, include

from posts import views

app_name = 'posts'

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comments')
router.register(r'history', views.HistoryViewSet)

urlpatterns = [
    path('child/', views.PostChildListApiView.as_view(), name='post-children'),
    path('post-comments/', views.PostCommentListAPIView.as_view(), name='post-comments'),
    path('comment-like/<int:comment_id>/', views.CommentLikeAPIView.as_view(), name='comment-like'),
    path('comment-replies/', views.CommentReplyListAPIView.as_view(), name='comment-replies'),
] + router.urls
