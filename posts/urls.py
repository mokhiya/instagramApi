from rest_framework.routers import DefaultRouter
from django.urls import path, include

from posts import views

app_name = 'posts'

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
                  path('child/', views.PostChildListApiView.as_view()),
              ] + router.urls
