from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('verify/resend/', views.ResendVerificationEmailView.as_view(), name='verify-resend'),
    path('me/', views.ProfileView.as_view(), name='profile'),
]