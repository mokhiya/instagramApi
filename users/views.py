import threading

from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.serializers import RegisterSerializer, VerificationSerializer, LoginSerializer, ResendCodeSerializer
from users.signals import send_verification_email


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()

    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerificationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_code = serializer.validated_data['user_code']
        user = user_code.user

        user.is_active = True
        user.save()
        user_code.delete()
        response = {
            'success': True,
            'message': 'Email Verified',
        }

        return Response(response, status=status.HTTP_200_OK)

class LoginView(APIView):
    serializer_class = LoginSerializer
    response = dict()
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(user=serializer.validated_data['user'])
        self.response['refresh'] = str(refresh)
        response = {
            'success': True,
            'refresh': str(refresh),
            'access_token': str(refresh.access_token)
        }
        return Response(response, status=status.HTTP_200_OK)


class ResendVerificationEmailView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_thread = threading.Thread(target=send_verification_email,
                                        args=(serializer.validated_data['email'],)).start()
        response = {
            'success': True,
            'message': 'New code is sent to your email',
        }
        return Response(response, status=status.HTTP_200_OK)


